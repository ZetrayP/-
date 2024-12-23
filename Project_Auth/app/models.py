from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime, timezone

def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    login_history: List["LoginHistory"] = Relationship(back_populates="user")
    tokens: List["TokenBlacklist"] = Relationship(back_populates="user")

class LoginHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    user_agent: str
    login_time: datetime = Field(default=get_utc_now)
    user: Optional[User] = Relationship(back_populates="login_history")

class TokenBlacklist(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    token: str = Field(index=True)
    user: Optional[User] = Relationship(back_populates="tokens")