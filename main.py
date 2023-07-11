from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import markdown
import uvicorn
import json

import database.data as DB

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
    while not shutdown:
        try:
            data : json = await websocket.receive_json()
            if data["id"] == "connection":
                response : str = await DB.sendFormConnection(form_=data)
                await websocket.send_text(json.dumps({"id" : data["id"], "message": response}))
            else:
                print("back-end not yet implemented")
        except WebSocketDisconnect as e:
            shutdown = True

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)