from sqlalchemy import text
from databases import Database
from asyncpg.exceptions import PostgresError
import json
import os

db: Database = None

async def initConnection():
    """ initialise the connection at the database """
    if not os.path.exists('database/config.json'):
        print("You need to have the file config.json in database/")
        return
    with open('database/config.json') as configConnection:
        connectInfo : json = json.load(configConnection)
    DATABASE_URL : str = f'postgresql://{connectInfo["user"]}:{connectInfo["password"]}@{connectInfo["host"]}:{connectInfo["port"]}/{connectInfo["database"]}'
    global db
    db = Database(DATABASE_URL)
    await db.connect()
    await testDatabaseConnection()

async def testDatabaseConnection():
    """ test the connection at the database """
    try:
        query = text("SELECT 1")
        await db.fetch_all(query)
        print("Database connection successful!")
    except Exception as e: 
        print(f"Error connecting to the database: {str(e)}")
        raise

async def closeDatabaseConnection():
    """ disconnect at the database """
    await db.disconnect()

async def sendFormConnection(form_ : json) -> str:
    """ Send request for connection """
    mail : str = form_['mail']
    password : str = form_['password']
    try : 
        query : text = text(f"SELECT * FROM Account WHERE email = '{mail}' AND password = crypt('{password}', password); ")
        results = await db.fetch_one(query)
        feedback : str
        if results is None:
            feedback = "bad email or password..." 
        else:
            results: dict = dict(results)
            results.pop("password")
            feedback = f"voici les infos du comptes : {results}"
        print(feedback)
        return feedback
    except PostgresError as e:
        print(f"Error from the database : {str(e)}")
        raise
    except Exception as e:
        print(f"Error : {str(e)}")
        raise

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
        feedback : str
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
        return "account created successfully !"
    except PostgresError as e:
        print(f"Error from the database : {str(e)}")
        raise
    except Exception as e:
        print(f"Error : {str(e)}")
        raise