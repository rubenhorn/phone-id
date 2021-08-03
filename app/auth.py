from fastapi_jwt_auth import AuthJWT

def create_access_token(Authorize: AuthJWT, current_user: str):
    return Authorize.create_access_token(subject=current_user)
    