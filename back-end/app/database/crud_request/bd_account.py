""" This File process request to BD """
# from asyncpg.exceptions import PostgresError
# from database.model import Account
# from sqlmodel import text
from logging import getLogger
from database.crud_request.base import CRUDBase
from database.model import Account
# import web_token.token as tk

# logger
logger = getLogger("vibraphile")


class Bd_account(CRUDBase[Account, Account, Account]):
    """
    process request to for account BD, using CRUD system
    """
    pass
