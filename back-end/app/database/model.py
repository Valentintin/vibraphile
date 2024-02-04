import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Account(Base):

    __tablename__ = 'Account'

    pseudonym = sa.Column(sa.String(16), primary_key=True)
    email = sa.Column(sa.String(50), nullable=False, unique=True)
    password = sa.Column(sa.String(50), nullable=False)
    createdAt = sa.Column(sa.Date(), nullable=False)
    lastLoginAt = sa.Column(sa.Date(), nullable=False)
    birthDate = sa.Column(sa.Date(), nullable=False)
    picture = sa.Column(sa.String(50), nullable=False)
    biography = sa.Column(sa.String(254))


class Document(Base):

    __tablename__ = 'Document'

    path = sa.Column(sa.String(50), primary_key=True)
    name = sa.Column(sa.String(16), nullable=False)
    type = sa.Column(sa.String(50), nullable=False)
    fileSize = sa.Column(sa.Integer(), nullable=False)
    createdAt = sa.Column(sa.Date(), nullable=False)
    lastModifiedAt = sa.Column(sa.Date(), nullable=False)
    lastVisitedAt = sa.Column(sa.String(50), nullable=False)
    description = sa.Column(sa.String(254))
    pseudonym = sa.Column(sa.String(16), sa.ForeignKey('Account.pseudonym'),
                          nullable=False)


class Read(Base):

    __tablename__ = 'read'

    pseudonym = sa.Column(sa.String(16), sa.ForeignKey('Account.pseudonym'),
                          primary_key=True)
    path = sa.Column(sa.String(50), sa.ForeignKey('Document.path'),
                     primary_key=True)
    lastVisitedAt = sa.Column(sa.Date(), nullable=False)


class Follow(Base):

    __tablename__ = 'Follow'

    pseudonymFollowed = sa.Column(sa.String(16),
                                  sa.ForeignKey('Account.pseudonym'),
                                  primary_key=True)
    pseudonymFollow = sa.Column(sa.String(16),
                                sa.ForeignKey('Account.pseudonym'),
                                primary_key=True)


class Evaluate(Base):

    __tablename__ = 'Evaluate'

    pseudonym = sa.Column(sa.String(16), sa.ForeignKey('Account.pseudonym'),
                          primary_key=True)
    path = sa.Column(sa.String(50), sa.ForeignKey('Document.path'),
                     primary_key=True)
    rating = sa.Column(sa.SmallInteger(), nullable=False)
    comment = sa.Column(sa.String(254), nullable=False)
    createdAt = sa.Column(sa.Date(), nullable=False)
