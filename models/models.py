from sqlalchemy import Column, Integer, VARCHAR, BigInteger

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    session_uuid = Column(VARCHAR(258), nullable=True, unique=True)

    def __str__(self):
        return f'<User:{self.id}>'
