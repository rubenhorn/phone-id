from constants import ROUTE_SEARCH, OP_ID_AUTHORIZE
from crud import get_user_ids_for_verified_phone_numbers
from typing import List
from fastapi import APIRouter
from fastapi_jwt_auth.auth_jwt import AuthJWT
from fastapi import APIRouter
from fastapi.params import Depends
from validation import validate_and_format_phone_number, InputException

router = APIRouter()

@router.post(ROUTE_SEARCH, operation_id=OP_ID_AUTHORIZE)
async def search(phone_numbers: List[str], Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    formatted_phone_numbers = []
    for phone_number in phone_numbers:
        try:
            formatted_phone_numbers.append(validate_and_format_phone_number(phone_number))
        except InputException:
            pass
    return get_user_ids_for_verified_phone_numbers(formatted_phone_numbers)