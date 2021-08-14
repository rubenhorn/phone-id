from fastapi.exceptions import HTTPException
from starlette.responses import JSONResponse
from crud import change_user_phone_number, create_user, get_user_by_id, get_user_by_phone_number, set_phone_number_verification_id
from validation import validate_and_format_phone_number
from fastapi.params import Depends, Form
from fastapi_jwt_auth.auth_jwt import AuthJWT
from constants import HTTP_CONFLICT, HTTP_CREATED, HTTP_NOT_FOUND, HTTP_OK, OP_ID_MAY_AUTHORIZE, ROUTE_REGISTER
from fastapi import APIRouter
from pydantic import BaseModel
from verification import get_phone_number_verification_service

router = APIRouter()
verification_service = get_phone_number_verification_service()

class __Registration(BaseModel):
    phone_number: str

@router.post(ROUTE_REGISTER, operation_id=OP_ID_MAY_AUTHORIZE)
async def __register(registration: __Registration, AuthJWT: AuthJWT = Depends()):
    formatted_phone_number = validate_and_format_phone_number(registration.phone_number)
    current_user_id = AuthJWT.get_jwt_subject()
    existing_phone_number_user = get_user_by_phone_number(
        formatted_phone_number)
    if existing_phone_number_user is not None and existing_phone_number_user.phone_number_verification_id is not None:
        # Pending verification for the same phone number must be canceled
        await verification_service.cancel_phone_number_verification(existing_phone_number_user.phone_number_verification_id)
    if current_user_id is None:  # Then register user
        phone_number_verification_id = await verification_service.send_verification_code(formatted_phone_number)
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
            phone_number_verification_id = await verification_service.send_verification_code(formatted_phone_number)
            change_user_phone_number(
                current_user_id, formatted_phone_number, phone_number_verification_id)
            return JSONResponse(status_code=HTTP_OK, content={'detail': 'User phone number changed and verification code sent'})
