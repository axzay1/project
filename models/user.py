from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255))
    phone_number = Column(String(20))
    authentication_provider = Column(String(50))
    role = Column(String(50))
    permissions = Column(String)
    password = Column(String)  # Or use ARRAY type for PostgreSQL


    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email}, password={self.password})>"
