from fastapi_jwt_auth.auth_jwt import AuthJWT
from pydantic.main import BaseModel
import config
from constants import *
from crud import *
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth.exceptions import AuthJWTException
from openapi import get_custom_openapi
from routers import register, verify, refresh, search
from starlette.requests import Request
from starlette.responses import JSONResponse
from validation import InputException
from verification.exceptions import *

if len(config.get(KEY_JWT_SECRET)) == 0:
    raise LookupError(f'Environmet variable { KEY_JWT_SECRET } not set')

class __Settings(BaseModel):
    authjwt_secret_key: str = config.get(KEY_JWT_SECRET)
    authjwt_algorithm: str = JWT_ALGORITHM

@AuthJWT.load_config
def get_config():
    return __Settings()

title = 'CollAction_PhoneID'
if config.get(KEY_USE_OPENAPI).lower() == 'true':
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
    return JSONResponse(status_code=status_code, content={'detail': 'Phone number verification failed'})

app.include_router(register.router)
app.include_router(verify.router)
app.include_router(refresh.router)
app.include_router(search.router)

app.openapi = get_custom_openapi(app)
