""" this file make all access to the database. """
# import
from sqlalchemy import text
from databases import Database
from asyncpg.exceptions import PostgresError
from logging import getLogger
import json
import os

import database.web_token as tk
# import database.model as ml

db: Database = None

# logger
logger = getLogger("vibraphile")


# setup
async def init_connection():
    """ initialise the connection at the database """
    if not os.path.exists('app/database/config.json'):
        logger.debug("need to have the file config.json in database/."
                     " Answer access from a developper.")
        return
    with open('app/database/config.json') as config_connection:
        connect_info: json = json.load(config_connection)
    DATABASE_URL: str = f'postgresql://{connect_info["user"]}:'\
                        f'{connect_info["password"]}@{connect_info["host"]}:'\
                        f'{connect_info["port"]}/{connect_info["database"]}'
    await tk.init_SECRET_KEY(connect_info["password"])
    global db
    db = Database(DATABASE_URL)
    await db.connect()
    await test_database_connection()


async def test_database_connection():
    """ test the connection at the database """
    try:
        query = text("SELECT 1")
        await db.fetch_all(query)
        logger.info("Database connection successful!")
    except Exception as e:
        logger.exception(f"Error connecting to the database: {str(e)}")
        raise


async def close_connection():
    """ disconnect at the database """
    await db.disconnect()

# Account #


async def connection(form_: json) -> dict:
    """ Send request for connection """
    mail: str = form_['mail']
    password: str = form_['password']
    try:
        query: text = text(f"SELECT * FROM Account WHERE email = '{mail}' AND password = crypt('{password}', password); ")
        results = await db.fetch_one(query)
        if results is None:
            return "bad email or password..."
        else:
            # Treat the results before send it
            results: dict = dict(results)
            results.pop("password")
            results["createdat"] = results["createdat"].isoformat()
            results["lastloginat"] = results["lastloginat"].isoformat()
            results["birthdate"] = results["birthdate"].isoformat()
            results["Token"]: str = tk.generate_token(results["pseudonym"])
            return results
    except PostgresError as e:
        logger.exception("An error occurred from the dataBase\n", exc_info=e)
        raise
    except Exception as e:
        logger.exception("An error occurred\n", exc_info=e)
        raise


async def test_connection(form_: json) -> str:
    """ test the connection with token """
    if tk.verify_token(form_["Token"]):
        return "connected !"
    else:
        return "not connected"


async def account_creation(form_: json) -> str:
    """ Send request for create a new account """
    pseudonym: str = form_['pseudonym']
    mail: str = form_['mail']
    password: str = form_['password']
    birthDate: str = form_['birthDate']
    try:

        # Verification for unique email and pseudonym
        email_query = text(f"SELECT email FROM Account WHERE email = '{mail}'")
        email_result = await db.fetch_one(email_query)
        if email_result:
            return "this email is already associted with an account"
        else:
            pseudonym_query = text(f"SELECT pseudonym FROM Account WHERE pseudonym = '{pseudonym}'")
            pseudonym_result = await db.fetch_one(pseudonym_query)
            if pseudonym_result:
                return "this pseudonym is already associted with an account"

        # create a new account
        query: text = text(f"INSERT INTO Account (pseudonym, email, password, createdAt, lastLoginAt, birthDate, picture) VALUES ('{pseudonym}', '{mail}', crypt('{password}', gen_salt('bf')), CURRENT_DATE, CURRENT_DATE, '{birthDate}', '');")
        await db.execute(query)
        os.makedirs(f"database/Storage/{pseudonym}", exist_ok=True)
        return "account created successfully !"
    except PostgresError as e:
        logger.exception("An error occurred from the database\n", exc_info=e)
        raise
    except Exception as e:
        logger.exception("An error occurred\n", exc_info=e)
        raise


async def account_delete(form_: json) -> str:
    """ Send request for delete an account """
    pseudonym: str = form_['pseudonym']
    password: str = form_['password']
    try:

        # Verification for unique pseudonym and password
        account_query = text(f"SELECT email FROM Account WHERE pseudonym = '{pseudonym}' AND password = crypt('{password}', password);")
        account_result = await db.fetch_one(account_query)
        if not account_result:
            return "bad password or pseudonym"
        # delete an account
        query: text = text(f""" DELETE FROM "account" WHERE pseudonym = '{pseudonym}'; """)
        await db.execute(query)
        return "account deleted successfully !"
    except PostgresError as e:
        logger.exception("An error occurred from the database\n", exc_info=e)
        raise
    except Exception as e:
        logger.exception("An error occurred\n", exc_info=e)
        raise


async def modify_account(form_: json) -> str:
    """ Send request for modify an Account """
    pseudonym: str = tk.verify_token(form_['Token'])
    if pseudonym:
        # see what to modify
        info_modify: str = form_["infoModify"]
        modification: str = form_["modification"]
        logger.debug(f"""infoModify : {info_modify} 
        && modification : {modification}""")
        # modify the information
        if info_modify == "password":
            query: text = text(f"UPDATE account SET {info_modify} = crypt('{modification}', password) WHERE pseudonym = '{pseudonym}';")
        else:
            query: text = text(f"UPDATE account SET {info_modify} = '{modification}' WHERE pseudonym = '{pseudonym}';")
        try:
            await db.execute(query)
            return "Info updated successfully !"
        except PostgresError as e:
            logger.exception("An error occurred from the database\n", exc_info=e)
            raise
        except Exception as e:
            logger.exception("An error occurred\n", exc_info=e)
            raise
    else:
        return "not correctly connected"

# Documents #


async def save_document(form_: json) -> str:
    """ Send request for save a new document """
    # Verify connexion
    pseudonym: str = tk.verify_token(form_['Token'])
    if not pseudonym:
        return "you need to be connected"
    # build the path
    name: str = form_['name']
    type: str = form_['type']
    path: str = f"database/Storage/{pseudonym}/{name}.{type}"
    # Verification for unique path
    if os.path.exists(path) and not form_['is_new']:
        return f"this document is already existing with the same path : {path} \n do you want to erase it ?"
    # Save the documents
    with open(path, "w") as f:
        f.write(form_['data'])
    # make a new row in database
    file_size: int = os.path.getsize(path)
    try:
        if form_['is_new']:
            query: text = text(f"INSERT INTO document ( path, name, type, fileSize, createdAt, lastModifiedAt, lastVisitedAt, pseudonym ) VALUES ('{path}', '{name}', '{type}', {file_size}, CURRENT_DATE, CURRENT_DATE, CURRENT_DATE, '{pseudonym}');")
        else:
            query: text = text(f"UPDATE document SET fileSize = {file_size}, lastModifiedAt = CURRENT_DATE, lastVisitedAt = CURRENT_DATE WHERE path = '{path}';")
        await db.execute(query)
        return "Document save successfully !"
    except PostgresError as e:
        logger.exception("An error occurred from the database\n", exc_info=e)
        raise
    except Exception as e:
        logger.exception("An error occurred\n", exc_info=e)
        raise


async def delete_document(form_: json) -> str:
    """ Send request for delete a document """
    # Verify connexion
    pseudonym: str = tk.verify_token(form_['Token'])
    if not pseudonym:
        return "you need to be connected"
    # build the path
    name: str = form_['name']
    type: str = form_['type']
    path: str = f"database/Storage/{pseudonym}/{name}.{type}"
    # Remove in the storage
    if os.path.exists(path):
        os.remove(path)
    # Remove in database
    try:
        query: text = text(f"DELETE FROM document WHERE path = '{path}';")
        await db.execute(query)
        return {"name": name}
    except PostgresError as e:
        logger.exception("An error occurred from the database\n", exc_info=e)
        raise
    except Exception as e:
        logger.exception("An error occurred\n", exc_info=e)
        raise


async def retrive_doc(form_: json) -> str | list:
    """ this function answer to request of documents for a specific user """
    # Verify connexion
    pseudonym: str = tk.verify_token(form_['Token'])
    if not pseudonym:
        return "you need to be connected"
    # make a request
    try:
        if form_['name']:
            doc_query = text(f"SELECT path FROM Document WHERE pseudonym = '{pseudonym}' AND name = '{form_['name']}'")
            doc_result = await db.fetch_one(doc_query)
            if not doc_result:
                return "no documents..."
            if os.path.exists(doc_result.path):
                with open(doc_result.path, "r") as f:
                    doc_content = f.read()
                return doc_content
            else:
                return "the documents is lost in storage... contact an admin"
        else:
            doc_query = text(f"SELECT name FROM Document WHERE pseudonym = '{pseudonym}'")
            doc_result = await db.fetch_all(doc_query)
            if not doc_result:
                return "no documents..."
            name_doc: list = [doc["name"] for doc in doc_result]
            return name_doc
    except PostgresError as e:
        logger.exception("An error occurred from the database\n", exc_info=e)
        raise
    except Exception as e:
        logger.exception("An error occurred\n", exc_info=e)
        raise
