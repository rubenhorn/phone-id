from models import User

def get_user_claims(user: User) -> dict:
    claims = dict()
    # TODO Token may not need to contain the user's phone number
    claims['phone_number'] = user.phone_number
    claims['phone_number_verified'] = user.phone_number_verified
    return claims