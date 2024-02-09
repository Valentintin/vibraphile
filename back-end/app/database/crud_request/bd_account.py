""" This File process request to BD """
from asyncpg.exceptions import PostgresError
from sqlalchemy.exc import IntegrityError
from logging import getLogger
from database.crud_request.base import CRUDBase
from database.model import Account
from web_token.token import generate_token
from sqlmodel import Session, text
from datetime import datetime
import os

# logger
logger = getLogger("vibraphile")


class Bd_account(CRUDBase[Account, Account, Account]):
    """
    process request to for account BD, using CRUD system
    """
    def connection(self, db: Session, email: str, password: str) -> dict:
        """ Send request for connection """
        try:
            query: text = text("SELECT pseudonym FROM Account WHERE "
                               "email = :email AND "
                               "password = crypt(:password, password);")
            params: dict = {'email': email, 'password': password}
            results = db.execute(query, params)
            res = results.first()
            if res is None:
                return "bad email or password..."
            else:
                finded = dict(res._mapping)
                # Treat the results before send it
                return generate_token(finded['pseudonym'])
        except PostgresError as e:
            logger.exception("An error occurred from the dataBase\n",
                             exc_info=e)
            raise
        except Exception as e:
            logger.exception("An error occurred\n", exc_info=e)
            raise

    def create(self, db: Session, *, obj_in: Account) -> str:
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
                            'pseudonym': pseudonym,
                            'birthdate': birthdate}
            db.execute(query, params)
            db.commit()
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

    def update(self, db: Session, *,
               pseudonym: str,
               obj_in: Account | dict[str, any]) -> Account:
        try:
            if not isinstance(obj_in, dict):
                obj_in: dict = obj_in.dict(exclude_unset=True)
            if 'password' in obj_in.keys():
                logger.debug("password update")
                query: text = text("UPDATE account SET password = "
                                   "crypt(:password, gen_salt('bf')) "
                                   "WHERE pseudonym = :pseudonym;")
                params: dict = {'password': obj_in.get('password'),
                                'pseudonym': obj_in.get('pseudonym')}
                db.execute(query, params)
                db.commit()
                obj_in.pop('password')
            db_obj = self.get(db, pseudonym)
            return super().update(db, db_obj=db_obj, obj_in=obj_in)
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
