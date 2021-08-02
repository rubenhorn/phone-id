import config
from constants import KEY_USE_POSTGRESQL_DIALECT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    if (config.get(KEY_USE_POSTGRESQL_DIALECT) or '').lower() == 'true':
        id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    else:
        uuid4_string = lambda: str(uuid.uuid4())
        id = Column(String, primary_key=True, default=uuid4_string)
    phone_number = Column(String, nullable=False, unique=True)
    phone_number_verified = Column(Boolean, default=False)
    phone_number_verification_id = Column(String)

#TODO delete this??
    def __repr__(self) -> str:
        return f'User(id="{ self.id }", phone_number="{ self.phone_number }", phone_number_verified="{ self.phone_number_verified }", phone_number_verification_id="{ self.phone_number_verification_id }")'
