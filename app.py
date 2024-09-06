from typing import Annotated

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

security = HTTPBasic()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/profile", response_class=HTMLResponse)
async def profile(
    request: Request, credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    if credentials.username.lower() == "admin":
        return RedirectResponse(url="/admin")

    return templates.TemplateResponse(
        "profile.html",
        {
            "request": request,
            "username": credentials.username,
        },
    )


@app.get("/admin", response_class=HTMLResponse)
async def admin_page(
    request: Request, credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    return templates.TemplateResponse("admin.html", {"request": request})


# TODO: LOGOUT