from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import markdown
import uvicorn
import json

import database.data as DB

from logs.log_config import init_logger
init_logger()
from logging import getLogger
logger = getLogger("musehik")

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
async def startup():
    await DB.initConnection()

@app.on_event("shutdown")
async def shutdown():
    await DB.closeDatabaseConnection()

@app.get('/markdown')
async def markdown(request: Request):
    return templates.TemplateResponse('markdown.html', {'request': request})

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})

@app.get("/connexion")
async def connexion(request: Request):
    return templates.TemplateResponse('connexion.html', {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    shutdown : bool = False
    response : str = ""
    while not shutdown:
        try:
            data : json = await websocket.receive_json()
            if data["id"] == "connection":
                response = await DB.sendFormConnection(form_=data)
            elif data["id"] == "testConnection":
                response = await DB.testConnection(form_=data)
            elif data["id"] == "saveDocument":
                response = await DB.saveDocument(form_=data)
            elif data["id"] == "accountCreation":
                response = await DB.sendFormAccountCreation(form_=data)
            elif data["id"] == "accountDelete":
                response = await DB.sendFormAccountDelete(form_=data)
            else:
                logger.error("back-end not yet implemented")
                break
            logger.debug(f'Response for {data["id"]} call is : {response}')
            await websocket.send_text(json.dumps({"id" : data["id"], "message": response}))
        except WebSocketDisconnect as e:
            shutdown = True

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)