from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

# class Base(DeclarativeBase):
#     pass

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    # Dynamic default and onupdate in UTC timezone
    created_at = Column(DateTime(timezone=True),
                          default=datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=datetime.now(
        timezone.utc), onupdate=datetime.now(timezone.utc))
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def __repr__(self):
        return f"<User {self.username} at {self.created_at}>"
