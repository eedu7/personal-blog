from typing import Annotated
from fastapi import Depends, FastAPI, Request, security
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

security = HTTPBasic()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def home(request: Request, credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    return templates.TemplateResponse("index.html", {"request": request, "username": credentials.username, "password": credentials.password})
