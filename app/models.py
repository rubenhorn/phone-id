import config
from constants import KEY_USE_POSTGRESQL_DIALECT, DB_TABLE_NAME_USER
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = DB_TABLE_NAME_USER
    if config.get(KEY_USE_POSTGRESQL_DIALECT).lower() == 'true':
        id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    else:
        uuid4_string = lambda: str(uuid.uuid4())
        id = Column(String, primary_key=True, default=uuid4_string)
    phone_number = Column(String, nullable=False, unique=True)
    phone_number_verified = Column(Boolean, default=False)
    phone_number_verification_id = Column(String)
