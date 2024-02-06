""" This File process request to BD """
from asyncpg.exceptions import PostgresError
from sqlalchemy.exc import IntegrityError
from logging import getLogger
from database.crud_request.base import CRUDBase
from database.model import Account
from sqlmodel import Session, text
from datetime import datetime
import os

# logger
logger = getLogger("vibraphile")


class Bd_account(CRUDBase[Account, Account, Account]):
    """
    process request to for account BD, using CRUD system
    """
    def create(self, db: Session, *, obj_in: Account) -> Account:
        try:
            email: str = obj_in.email
            password: str = obj_in.password
            pseudonym: str = obj_in.pseudonym
            birthdate: str = datetime.fromisoformat(obj_in.birthdate)
            query: text = text("INSERT INTO Account (pseudonym, email,"
                               " password, createdAt, lastLoginAt, birthDate,"
                               " picture) VALUES (:pseudonym, :email,"
                               " crypt(:password, gen_salt('bf')),"
                               " CURRENT_DATE, CURRENT_DATE,"
                               " :birthdate, '');")
            params: dict = {'email': email, 'password': password,
                            'pseudonym': pseudonym, 'birthdate': birthdate}
            db.execute(query, params)
            os.makedirs(f"app/database/Storage/{pseudonym}", exist_ok=True)
            return "account created successfully !"
        except IntegrityError as e:
            if "duplicate key value violates unique constraint" in str(e):
                logger.exception("pseudo or email already picked...\n")
                raise
        except PostgresError as e:
            logger.exception("An error occurred from the database\n",
                             exc_info=e)
            raise
        except Exception as e:
            logger.exception("An error occurred\n", exc_info=e)
            raise
