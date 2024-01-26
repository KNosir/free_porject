from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import DeclarativeBase, Session


class Base(DeclarativeBase):
    pass

class UserAccounts(Base):
    __tablename__ = "user_account"
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String)
    account_number = Column(Integer, unique=True)
    balance = Column(Integer, default=10000)
    is_deleted = Column(Boolean, default=False)


