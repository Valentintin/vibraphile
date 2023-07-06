from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import markdown
import uvicorn

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

@app.post("/formConnexion")
async def TryConnexion(request: Request):
    form = await request.form()
    await DB.sendFormConnection(form_=form)
    return HTMLResponse(status_code=204)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)