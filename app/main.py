from starlette.responses import JSONResponse
import config
from constants import *
from crud import *
from fastapi import FastAPI, Depends
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Form
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.openapi.utils import get_openapi
from models import User
from pydantic.main import BaseModel
from starlette.requests import Request
from validation import validate_and_format_phone_number, validate_verification_code, InputException
from verification import *

if config.get(KEY_JWT_SECRET) is None:
    raise LookupError(f'Environmet variable { KEY_JWT_SECRET } not set')

title = 'CollAction_phone-auth'
if (config.get(KEY_USE_OPENAPI) or '').lower() == 'true':
    app = FastAPI(title=title, redoc_url=None)
else:
    app = FastAPI(title=title, redoc_url=None, docs_url=None, openapi_url=None)
create_database()


class Settings(BaseModel):
    authjwt_secret_key: str = config.get(KEY_JWT_SECRET)


@AuthJWT.load_config
def get_config():
    return Settings()


@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={'detail': exc.detail})


@app.exception_handler(AuthJWTException)
async def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=HTTP_BAD_REQUEST, content={'detail': str(exc)})


@app.exception_handler(InputException)
async def input_exception_handler(request: Request, exc: InputException):
    return JSONResponse(status_code=HTTP_BAD_REQUEST, content={'detail': str(exc)})


@app.exception_handler(VerificationException)
async def verification_exception_handler(request: Request, exc: VerificationException):
    status_code = HTTP_INTERNAL_SERVER_ERROR
    if isinstance(exc, VerificationCodeCheckException):
        status_code = HTTP_UNPROCESSABLE_ENTITY
    return JSONResponse(status_code=status_code, content={'detail': str(exc)})


@app.post(ROUTE_REGISTER, operation_id=OP_ID_MAY_AUTHORIZE)
async def register(phone_number: str = Form(...), AuthJWT: AuthJWT = Depends()):
    formatted_phone_number = validate_and_format_phone_number(phone_number)
    current_user_id = AuthJWT.get_jwt_subject()
    existing_phone_number_user = get_user_by_phone_number(
        formatted_phone_number)
    if current_user_id is None:  # Then register user
        phone_number_verification_id = await send_verification_code(formatted_phone_number)
        # New user registering
        if existing_phone_number_user is None:
            create_user(formatted_phone_number, phone_number_verification_id)
            return JSONResponse(status_code=HTTP_CREATED, content={'detail': 'User created and verification code sent'})
        # Existing user registering (on other device or after logoout)
        else:
            set_phone_number_verification_id(
                existing_phone_number_user.id, phone_number_verification_id)
            return JSONResponse(status_code=HTTP_OK, content={'detail': 'Verification code sent'})
    else:  # Then change phone number
        # Phone number is already registered to other user
        if existing_phone_number_user is not None and existing_phone_number_user.phone_number_verified:
            raise HTTPException(status_code=HTTP_CONFLICT,
                                detail='Phone number already registered')
        # User does no longer exist
        elif get_user_by_id(current_user_id) is None:
            raise HTTPException(status_code=HTTP_NOT_FOUND,
                                detail='User not found')
        # Update phone number
        else:
            phone_number_verification_id = await send_verification_code(formatted_phone_number)
            change_user_phone_number(
                current_user_id, formatted_phone_number, phone_number_verification_id)
            return JSONResponse(status_code=HTTP_OK, content={'detail': 'User phone number changed and verification code sent'})


def create_access_token(Authorize: AuthJWT, current_user: str):
    return Authorize.create_access_token(subject=current_user)


@app.post(ROUTE_LOGIN)
async def login(phone_number: str = Form(...), verification_code: str = Form(...), Authorize: AuthJWT = Depends()):
    formatted_phone_number = validate_and_format_phone_number(phone_number)
    validate_verification_code(verification_code)
    current_user: User = get_user_by_phone_number(formatted_phone_number)
    if current_user is None:
        raise HTTPException(status_code=HTTP_NOT_FOUND,
                            detail='User not found (Please register!)')
    if current_user.phone_number_verification_id is None:
        raise HTTPException(status_code=HTTP_BAD_REQUEST,
                            detail='User not verified (Please send verification code)')
    await verify_phone_number(phone_number, current_user.phone_number_verification_id, verification_code)
    mark_user_phone_number_as_verified(current_user.id)
    access_token = create_access_token(Authorize, current_user.id)
    refresh_token = Authorize.create_refresh_token(
        subject=current_user.id, expires_time=False)  # TODO add token invalidation later?
    return {'access_token': access_token, 'refresh_token': refresh_token}


@app.post(ROUTE_REFRESH, operation_id=OP_ID_AUTHORIZE)
async def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()
    current_user: str = Authorize.get_jwt_subject()
    new_token = create_access_token(Authorize, current_user)
    return {'access_token': new_token}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title, version=app.version, routes=app.routes)

    router_authorize = [route for route in app.routes[3:]
                        if route.operation_id in [OP_ID_AUTHORIZE, OP_ID_MAY_AUTHORIZE]]
    for route in router_authorize:
        print(route.path)
        method = list(route.methods)[0].lower()
        additional_header = {'name': 'Authorization', 'in': 'header', 'schema': {
            'title': 'Authorization', 'type': 'string'}, 'required': route.operation_id == OP_ID_AUTHORIZE}
        try:
            openapi_schema['paths'][route.path][method]['parameters'].append(
                additional_header)
        except Exception:
            openapi_schema['paths'][route.path][method].update(
                {'parameters': [additional_header]})

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
