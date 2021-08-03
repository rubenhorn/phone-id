import config
from constants import *
from crud import *
from fastapi import FastAPI, Depends
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Form
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from models import User
from openapi import get_custom_openapi
from pydantic.main import BaseModel
from routers import register, login, refresh
from starlette.requests import Request
from starlette.responses import JSONResponse
from validation import validate_and_format_phone_number, validate_verification_code, InputException
from verification import *
from verification.mock import MockPhoneVerificationService

if config.get(KEY_JWT_SECRET) is None:
    raise LookupError(f'Environmet variable { KEY_JWT_SECRET } not set')

class Settings(BaseModel):
    authjwt_secret_key: str = config.get(KEY_JWT_SECRET)

@AuthJWT.load_config
def get_config():
    return Settings()

verification_service: PhoneVerificationService = MockPhoneVerificationService()

title = 'CollAction_phone-auth'
if (config.get(KEY_USE_OPENAPI) or '').lower() == 'true':
    app = FastAPI(title=title, redoc_url=None)
else:
    app = FastAPI(title=title, redoc_url=None, docs_url=None, openapi_url=None, debug=False)
create_database()

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

app.include_router(register.router)
app.include_router(login.router)
app.include_router(refresh.router)

app.openapi = get_custom_openapi(app)
