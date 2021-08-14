from sqlalchemy.sql.expression import true
from models import User

def get_user_claims(user: User) -> dict:
    claims = dict()
    claims['phone_number'] = user.phone_number
    claims['phone_number_verified'] = True # Tokens are only issued after verification
    return claims