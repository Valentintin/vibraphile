from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import json

def initConnection(app : Flask):
    """ initialise the connection at the database """
    with open('database/config.json') as configConnection:
        connect = json.load(configConnection)
    global db
    db = SQLAlchemy()
    app.config["SQLALCHEMY_DATABASE_URI"] = f'postgresql://{connect["user"]}:{connect["password"]}@{connect["host"]}:{connect["port"]}/{connect["database"]}'
    db.init_app(app)

def sendFormConnection(request_ : request):
    """ Send request for connection """
    mail : str = request_.form['mail']
    password : str = request_.form['password']
    try : 
        query : text = text(f"SELECT * FROM Account WHERE email = '{mail}' AND password = crypt('{password}', password); ")
        print(query)
        results = db.session.execute(query)
    except :
        print(f"erreur, mauvaise email ou mot de passe")
        return
    print(f"voici les infos du comptes {results.all()}")
    return results
