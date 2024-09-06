from typing import Annotated

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from crud import get_all, delete_article

app = FastAPI()

security = HTTPBasic()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# TODO: Delete is not working
# TODO: EDIT not implemented

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    articles = get_all()
    return templates.TemplateResponse("index.html", {"request": request, "articles": articles})


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

@app.post("/edit/{article_id}")
def delete_article_endpoint(article_id: str, credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    delete_article(article_id)
    if credentials.username.lower() == "admin":
        return RedirectResponse(url="/admin")
    return RedirectResponse(url="/profile")

# TODO: LOGOUT