from auth import create_access_token
from fastapi.params import Depends
from fastapi_jwt_auth.auth_jwt import AuthJWT
from constants import OP_ID_AUTHORIZE, ROUTE_REFRESH
from fastapi import APIRouter

router = APIRouter()

@router.post(ROUTE_REFRESH, operation_id=OP_ID_AUTHORIZE)
async def __refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()
    current_user: str = Authorize.get_jwt_subject()
    new_token = create_access_token(Authorize, current_user)
    return {'access_token': new_token}
