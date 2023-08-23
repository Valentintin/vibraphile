#import
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import markdown
import uvicorn
import json

import database.data as db

#logger
from logs.log_config import init_logger
init_logger()
from logging import getLogger
logger = getLogger("musehik")

#setup app
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
async def startup():
    """ event call on the startup of the application """
    await db.init_connection()

@app.on_event("shutdown")
async def shutdown():
    """ event call on the shutdown of the application """
    await db.close_connection()

@app.get("/")
async def home(request: Request):
    """ used for load a page """
    return templates.TemplateResponse('index.html', {"request": request})

@app.get("/connexion")
async def connexion(request: Request):
    """ used for load a page """
    return templates.TemplateResponse('connexion.html', {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """ websocket bilateral communication """
    await websocket.accept()
    shutdown : bool = False
    response : str = ""
    while not shutdown:
        try:
            #receive from the front
            data : json = await websocket.receive_json()
            if data["id"] == "connection":
                response = await db.sendFormConnection(form_=data)
            elif data["id"] == "testConnection":
                response = await db.test_connection(form_=data)
            elif data["id"] == "saveDocument":
                response = await db.save_document(form_=data)
            elif data["id"] == "retriveDoc":
                response = await db.retrive_doc(form_=data)
            elif data["id"] == "accountCreation":
                response = await db.account_creation(form_=data)
            elif data["id"] == "accountDelete":
                response = await db.account_delete(form_=data)
            elif data["id"] == "modifyAccount":
                response = await db.modify_account(form_=data)
            else:
                logger.error("back-end not yet implemented")
                break

            #answer to the front
            logger.debug(f'Response for {data["id"]} call is : {response}')
            await websocket.send_text(json.dumps({"id" : data["id"], "message": response}))
        except WebSocketDisconnect as e:
            shutdown = True

#start the server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)