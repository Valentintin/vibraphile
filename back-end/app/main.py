""" this file is the core of the back-end system. this is where the exchange
with the front-end append """
# import
from fastapi import FastAPI, Request  # , WebSocket, WebSocketDisconnect
from contextlib import asynccontextmanager
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

import database.bd_setup as bd_setup
from database.model import UserIn
from routers import accounts
from web_token.token import init_SECRET_KEY

# logger
from logs.log_config import init_logger
from logging import getLogger
init_logger()
logger = getLogger("vibraphile")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """ lifespan define what to do before launch, and before close """
    await bd_setup.init_connection()
    await init_SECRET_KEY()
    yield


# setup app
app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(accounts.router)


@app.get("/")
async def home(request: Request):
    """ used for load a page """
    return templates.TemplateResponse('index.html', {"request": request})


@app.get("/connexion")
async def connexion(request: Request):
    """ used for load a page """
    return templates.TemplateResponse('connexion.html', {"request": request})


@app.post("/Account/login")
async def login(userIn: UserIn) -> str:
    return await bd_setup.connection(userIn.email, userIn.password)


# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     """ websocket bilateral communication """
#     await websocket.accept()
#     response: str = ""

#     async def process_response(data: json):
#         """ this function make the route with the fonction used in data """
#         if data["id"] == "connection":
#             response = await db.connection(form_=data)
#         elif data["id"] == "testConnection":
#             response = await db.test_connection(form_=data)
#         elif data["id"] == "saveDocument":
#             response = await db.save_document(form_=data)
#         elif data["id"] == "deleteDocument":
#             response = await db.delete_document(form_=data)
#         elif data["id"] == "retriveDoc":
#             response = await db.retrive_doc(form_=data)
#         elif data["id"] == "accountCreation":
#             response = await db.account_creation(form_=data)
#         elif data["id"] == "accountDelete":
#             response = await db.account_delete(form_=data)
#         elif data["id"] == "modifyAccount":
#             response = await db.modify_account(form_=data)
#         else:
#             logger.error("back-end not yet implemented")
#             response = "back-end not yet implemented"
#         return response

#     while True:
#         try:
#             data: json = await websocket.receive_json()  # from the front

#             response = await process_response(data)

#             logger.debug(f'Response for {data["id"]} call is : {response}')
#             await websocket.send_text(json.dumps({
#                 "id": data["id"],
#                 "message": response}))  # to the front
#         except WebSocketDisconnect:
#             break
#         except Exception as e:
#             logger.exception("error from a response process")
#             await websocket.send_text(json.dumps({
#                 "id": data["id"],
#                 "message": str(e)}))

# start the server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
