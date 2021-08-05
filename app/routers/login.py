from fastapi.exceptions import HTTPException
from models import User
from crud import get_user_by_phone_number, mark_user_phone_number_as_verified
from validation import validate_and_format_phone_number, validate_verification_code
from fastapi_jwt_auth.auth_jwt import AuthJWT
from constants import HTTP_NOT_FOUND, ROUTE_LOGIN, HTTP_BAD_REQUEST
from fastapi import APIRouter
from fastapi.params import Depends, Form
from verification import get_phone_number_verification_service

router = APIRouter()
verification_service = get_phone_number_verification_service()

@router.post(ROUTE_LOGIN)
async def login(phone_number: str = Form(...), verification_code: str = Form(...), Authorize: AuthJWT = Depends()):
    formatted_phone_number = validate_and_format_phone_number(phone_number)
    validate_verification_code(verification_code)
    current_user: User = get_user_by_phone_number(formatted_phone_number)
    if current_user is None:
        raise HTTPException(status_code=HTTP_NOT_FOUND,
                            detail='User not found (Please register!)')
    if current_user.phone_number_verification_id is None:
        raise HTTPException(status_code=HTTP_BAD_REQUEST,
                            detail='No pending registration found (Please register!)')
    await verification_service.verify_phone_number(phone_number, current_user.phone_number_verification_id, verification_code)
    mark_user_phone_number_as_verified(current_user.id)
    subject = str(current_user.id)
    access_token = Authorize.create_access_token(subject=subject)
    refresh_token = Authorize.create_refresh_token(
        subject=subject, expires_time=False)  # TODO add token invalidation later?
    return {'access_token': access_token, 'refresh_token': refresh_token}