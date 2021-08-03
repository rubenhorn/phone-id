import config
from constants import *
from models import Base, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys

def __get_db_url():
    user = config.get(KEY_POSTGRESQL_USER)
    password = config.get(KEY_POSTGRESQL_PASS)
    host = config.get(KEY_POSTGRESQL_HOST)
    port = config.get(KEY_POSTGRESQL_PORT)
    db = config.get(KEY_POSTGRESQL_DB)
    if len([v for v in [user, password, host, port, db] if v is None or v.strip() is '']) != 0:
        print('Incomplete PostgreSQL configuration (Falling back on ephemeral in-memory sqlite database)', file=sys.stderr)
        db_url = 'sqlite:///'
    else:
        db_url = f'postgres+psycopg2://{user}:{password}@{host}:{port}/{db}'
    return db_url

__engine = create_engine(__get_db_url(), echo=False)

def __create_session():
    Session = sessionmaker(bind=__engine)
    return Session()

def create_database():
    Base.metadata.create_all(bind=__engine)

def recreate_database():
    Base.metadata.drop_all(bind=__engine)
    create_database()

def create_user(phone_number, phone_number_verification_id):
    with __create_session() as Session:
        user = User(phone_number=phone_number, phone_number_verification_id=phone_number_verification_id)
        Session.add(user)
        Session.commit()

def set_phone_number_verification_id(id, phone_number_verification_id):
    with __create_session() as Session:
        user = Session.query(User).filter_by(id=id).first()
        user.phone_number_verification_id = phone_number_verification_id
        Session.commit()

def get_user_by_id(id):
    with __create_session() as Session:
        return Session.query(User).filter_by(id=id).first()

def get_user_by_phone_number(phone_number):
    with __create_session() as Session:
        return Session.query(User).filter_by(phone_number=phone_number).first()

def mark_user_phone_number_as_verified(id):
    with __create_session() as Session:
        user = Session.query(User).filter_by(id=id).first()
        user.phone_number_verified = True
        user.phone_number_verification_id = None
        Session.commit()

def change_user_phone_number(id, new_phone_number, phone_number_verification_id):
    with __create_session() as Session:
        user = Session.query(User).filter_by(id=id).first()
        user.phone_number = new_phone_number
        user.phone_number_verified = False
        phone_number_verification_id = phone_number_verification_id
        Session.commit()
