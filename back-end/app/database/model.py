from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime


class Account(SQLModel, table=True, arbitrary_types_allowed=True):
    pseudonym: str = Field(primary_key=True)
    email: Optional[str] = None
    password: Optional[str] = None
    createdat: Optional[datetime] = None
    lastloginat: Optional[datetime] = None
    birthdate: datetime = None
    picture: Optional[str] = None
    biography: Optional[str] = None


class Document(SQLModel, table=True):
    path: str = Field(primary_key=True)
    name: str
    type: str
    filesize: int
    createdat: datetime
    lastmodifiedat: datetime
    lastvisitedat: datetime
    description: Optional[str] = None
    pseudonym: str = Field(foreign_key="Account.pseudonym")
