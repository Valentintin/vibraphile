from fastapi import Form
from sqlalchemy import text
from databases import Database
from asyncpg.exceptions import PostgresError
import json

db: Database = None

async def initConnection():
    """ initialise the connection at the database """
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
        print("Error connecting to the database:", e)
        raise

async def closeDatabaseConnection():
    """ disconnect at the database """
    await db.disconnect()

async def sendFormConnection(form_ : Form):
    """ Send request for connection """
    mail : str = form_['mail']
    password : str = form_['password']
    try : 
        query : text = text(f"SELECT * FROM Account WHERE email = '{mail}' AND password = crypt('{password}', password); ")
        print(query)
        results = await db.fetch_one(query)
        if results is None:
            print("bad email or password...")
        else:
            print(f"voici les infos du comptes {dict(results)} : ")
    except PostgresError as e:
        print(f"Error from the database : {str(e)}")
    except Exception as e:
        print(f"Error : {str(e)}")