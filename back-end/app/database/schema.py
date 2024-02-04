import datetime
from typing import Optional
from pydantic import BaseModel


class Account(BaseModel):

    pseudonym: str
    email: str
    password: str
    createdAt: datetime.date
    lastLoginAt: datetime.date
    birthDate: datetime.date
    picture: str
    biography: Optional[str]


class Document(BaseModel):

    path: str
    name: str
    type: str
    fileSize: int
    createdAt: datetime.date
    lastModifiedAt: datetime.date
    lastVisitedAt: str
    description: Optional[str]
    pseudonym: str


class Read(BaseModel):

    pseudonym: str
    path: str
    lastVisitedAt: datetime.date


class Follow(BaseModel):

    pseudonymFollowed: str
    pseudonymFollow: str


class Evaluate(BaseModel):

    pseudonym: str
    path: str
    rating: int
    comment: str
    createdAt: datetime.date
