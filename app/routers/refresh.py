from auth import get_user_claims
from constants import HTTP_NOT_FOUND
from crud import get_user_by_id
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from fastapi_jwt_auth.auth_jwt import AuthJWT
from constants import OP_ID_AUTHORIZE, ROUTE_REFRESH

router = APIRouter()

@router.post(ROUTE_REFRESH, operation_id=OP_ID_AUTHORIZE)
async def __refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()
    subject: str = Authorize.get_jwt_subject()
    current_user = get_user_by_id(subject)
    if current_user is None:
        raise HTTPException(status_code=HTTP_NOT_FOUND,
                            detail='User does not exist (Deleted)')
    new_token = Authorize.create_access_token(subject=subject, user_claims=get_user_claims())
    return {'access_token': new_token}
