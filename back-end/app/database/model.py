from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime


class UserIn(SQLModel):
    email: str
    password: str


class Account(SQLModel, table=True, arbitrary_types_allowed=True):
    pseudonym: str = Field(primary_key=True)
    email: Optional[str] = None
    password: Optional[str]
    createdAt: Optional[datetime] = None
    lastLoginAt: Optional[datetime] = None
    birthDate: datetime
    picture: Optional[str] = None
    biography: Optional[str] = None
    token: Optional[str] = None


class Document(SQLModel, table=True):
    path: str = Field(primary_key=True)
    name: str
    type: str
    fileSize: int
    createdAt: datetime
    lastModifiedAt: datetime
    lastVisitedAt: datetime
    description: Optional[str] = None
    pseudonym: str = Field(foreign_key="Account.pseudonym")
