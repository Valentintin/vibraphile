from sqlalchemy import text
from databases import Database
from asyncpg.exceptions import PostgresError
import json
import os

import database.token as tk

db : Database = None

from logging import getLogger
logger = getLogger("musehik")

async def initConnection():
    """ initialise the connection at the database """
    if not os.path.exists('database/config.json'):
        logger.debug("You need to have the file config.json in database/")
        return
    with open('database/config.json') as configConnection:
        connectInfo : json = json.load(configConnection)
    DATABASE_URL : str = f'postgresql://{connectInfo["user"]}:{connectInfo["password"]}@{connectInfo["host"]}:{connectInfo["port"]}/{connectInfo["database"]}'
    await tk.initSECRET_KEY(connectInfo["password"])
    global db
    db = Database(DATABASE_URL)
    await db.connect()
    await testDatabaseConnection()

async def testDatabaseConnection():
    """ test the connection at the database """
    try:
        query = text("SELECT 1")
        await db.fetch_all(query)
        logger.info("Database connection successful!")
    except Exception as e: 
        logger.error(f"Error connecting to the database: {str(e)}")
        raise

async def closeDatabaseConnection():
    """ disconnect at the database """
    await db.disconnect()

### Account ###

async def sendFormConnection(form_ : json) -> str|dict:
    """ Send request for connection """
    mail : str = form_['mail']
    password : str = form_['password']
    try : 
        query : text = text(f"SELECT * FROM Account WHERE email = '{mail}' AND password = crypt('{password}', password); ")
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
            results["Token"] : str = tk.generate_token(results["pseudonym"])
            return results
    except PostgresError as e:
        logger.exception("An error occurred from the dataBase\n", exc_info=e)
        raise
    except Exception as e:
        logger.exception("An error occurred\n", exc_info=e)
        raise

async def testConnection(form_ : json) -> str:
    """ test the connection with token """
    if tk.verify_token(form_["Token"]):
        return "connected !"
    else:
        return "not connected"

async def sendFormAccountCreation(form_ : json) -> str:
    """ Send request for create a new account """
    pseudonym : str = form_['pseudonym']
    mail : str = form_['mail']
    password : str = form_['password']
    birthDate : str = form_['birthDate']
    try :

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
        query : text = text(f"INSERT INTO Account (pseudonym, email, password, createdAt, lastLoginAt, birthDate, picture) VALUES ('{pseudonym}', '{mail}', crypt('{password}', gen_salt('bf')), CURRENT_DATE, CURRENT_DATE, '{birthDate}', '');")
        await db.execute(query)
        os.makedirs(f"database/Storage/{pseudonym}", exist_ok=True)
        return "account created successfully !"
    except PostgresError as e:
        logger.exception("An error occurred from the database\n", exc_info=e)
        raise
    except Exception as e:
        logger.exception("An error occurred\n", exc_info=e)
        raise

async def sendFormAccountDelete(form_ : json) -> str:
    """ Send request for delete an account """
    pseudonym : str = form_['pseudonym']
    password : str = form_['password']
    try :

        # Verification for unique pseudonym and password
        account_query = text(f"SELECT email FROM Account WHERE pseudonym = '{pseudonym}' AND password = crypt('{password}', password);")
        account_result = await db.fetch_one(account_query)
        if not account_result:
            return "bad password or pseudonym"
        # delete an account
        query : text = text(f""" DELETE FROM "account" WHERE pseudonym = '{pseudonym}'; """)
        await db.execute(query)
        return "account deleted successfully !"
    except PostgresError as e:
        logger.exception("An error occurred from the database\n", exc_info=e)
        raise
    except Exception as e:
        logger.exception("An error occurred\n", exc_info=e)
        raise

async def sendFormModifyAccount(form_ : json) -> str:
    """ Send request for modify an Account """
    pseudonym : str = tk.verify_token(form_['Token'])
    if pseudonym:
        pass
        # see what to modify
        infoModify : str = form_["infoModify"]
        modification : str = form_["modification"]
        logger.debug(f"infoModify : {infoModify} && modification : {modification}")
        # modify the information
        try:
            query : text = text(f"UPDATE account SET {infoModify} = '{modification}' WHERE pseudonym = '{pseudonym}';")
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

### Documents ###

async def saveDocument(form_ : json) -> str:
    """ Send request for save a new document """
    # Verify connexion
    pseudonym : str = tk.verify_token(form_['Token'])
    if not pseudonym:
        return "you need to be connected"
    # build the path
    name : str = form_['name']
    type : str = form_['type']
    path : str = f"database/Storage/{pseudonym}/{name}.{type}"
    # Verification for unique path
    if os.path.exists(path) and not form_['is_new']:
        return f"this document is already existing with the same path : {path} \n do you want to erase it ?"
    # Save the documents
    with open(path, "w") as f:
        f.write(form_['data'])
    # make a new row in database
    fileSize : int = os.path.getsize(path)
    try:
        if form_['is_new']:
            query : text = text(f"INSERT INTO document ( path, name, type, fileSize, createdAt, lastModifiedAt, lastVisitedAt, pseudonym ) VALUES ('{path}', '{name}', '{type}', {fileSize}, CURRENT_DATE, CURRENT_DATE, CURRENT_DATE, '{pseudonym}');")
        else:
            query : text = text(f"UPDATE document SET fileSize = {fileSize}, lastModifiedAt = CURRENT_DATE, lastVisitedAt = CURRENT_DATE WHERE path = '{path}';")
        await db.execute(query)
        return "Document save successfully !"
    except PostgresError as e:
        logger.exception("An error occurred from the database\n", exc_info=e)
        raise
    except Exception as e:
        logger.exception("An error occurred\n", exc_info=e)
        raise

async def retrive_doc(form_ : json) -> str|list:
    """ this function answer to request of documents for a specific user """
    # Verify connexion
    pseudonym : str = tk.verify_token(form_['Token'])
    if not pseudonym:
        return "you need to be connected"
    # make a request
    try :
        if form_['name']:
            doc_query = text(f"SELECT path FROM Document WHERE pseudonym = '{pseudonym}' AND name = '{form_['name']}'")
            doc_result = await db.fetch_one(doc_query)
            if not doc_result:
                return "no documents..."
            with open(doc_result.path, "r") as f:
                doc_content = f.read()
            return doc_content
        else:
            doc_query = text(f"SELECT name FROM Document WHERE pseudonym = '{pseudonym}'")
            doc_result = await db.fetch_all(doc_query)
            if not doc_result:
                return "no documents..."
            name_doc : list = [doc["name"] for doc in doc_result]
            return name_doc
    except PostgresError as e:
        logger.exception("An error occurred from the database\n", exc_info=e)
        raise
    except Exception as e:
        logger.exception("An error occurred\n", exc_info=e)
        raise