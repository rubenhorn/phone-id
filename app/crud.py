from session import get_engine, create_session
from models import Base, User

def create_database():
    Base.metadata.create_all(bind=get_engine())

def recreate_database():
    Base.metadata.drop_all(bind=get_engine())
    create_database()

def create_user(phone_number, phone_number_verification_id):
    with create_session() as Session:
        user = User(phone_number=phone_number, phone_number_verification_id=phone_number_verification_id)
        Session.add(user)
        Session.commit()

def set_phone_number_verification_id(id, phone_number_verification_id):
    with create_session() as Session:
        user = Session.query(User).filter_by(id=id).first()
        user.phone_number_verification_id = phone_number_verification_id
        Session.commit()

def get_user_by_id(id):
    with create_session() as Session:
        return Session.query(User).filter_by(id=id).first()

def get_user_by_phone_number(phone_number):
    with create_session() as Session:
        return Session.query(User).filter_by(phone_number=phone_number).first()

def mark_user_phone_number_as_verified(id):
    with create_session() as Session:
        user = Session.query(User).filter_by(id=id).first()
        user.phone_number_verified = True
        user.phone_number_verification_id = None
        Session.commit()

def change_user_phone_number(id, new_phone_number, phone_number_verification_id):
    with create_session() as Session:
        user = Session.query(User).filter_by(id=id).first()
        user.phone_number = new_phone_number
        user.phone_number_verified = False
        phone_number_verification_id = phone_number_verification_id
        Session.commit()
