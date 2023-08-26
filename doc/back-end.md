# Back-end documentation

the back-end system is principaly used for launching the server, create a stable connection, communicate with the front, send request to the database.

## Dependances

The code was write under python 3.11. We used [FastAPI](https://fastapi.tiangolo.com/fr/) as ASGI framework for the back-end.

You can see all python dependancies in requirement.txt, and install every things with :
```
pip install -r requirement.txt
```
You need to ask config.json file how gave access to the postgre database, and give your public IP to have completed control.

## explication

- **[main.py](../main.py)** is the file how launch the server. With a websocket we make a bilateral communication with the front-end.

- **[data.py](../database/data.py)** contain function for access of the database. This is where we send all postgresql request.

- **[token.py](../database/token.py)** manage the connection with token. It's permit to have a stable connection for the user.

- **[log_config.py](../logs/log_config.py)** is the configuration of the logger used anywhere in the code.
