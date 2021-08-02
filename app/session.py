import config
from constants import *
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
        __db_url = 'sqlite:///'
    else:
        __db_url = f'postgres+psycopg2://{user}:{password}@{host}:{port}/{db}'
    return __db_url

__engine = create_engine(__get_db_url(), echo=False)

def get_engine():
    return __engine

def create_session():
    Session = sessionmaker(bind=get_engine())
    return Session()
