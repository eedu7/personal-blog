from typing import Annotated
from urllib import response

from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import urllib

from crud import delete_article, get_all, add_article, get_by_id

app = FastAPI()

security = HTTPBasic()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

class CustomURLProcessor:
    def __init__(self):  
        self.path = "" 
        self.request = None

    def url_for(self, request: Request, name: str, **params: str):
        self.path = request.url_for(name, **params)
        self.request = request
        return self
    
    def include_query_params(self, **params: str):
        parsed = list(urllib.parse.urlparse(self.path))
        parsed[4] = urllib.parse.urlencode(params)
        return urllib.parse.urlunparse(parsed)


# TODO: EDIT not implemented


@app.get("/", response_class=HTMLResponse)
async def home_endpoint(request: Request):
    articles = get_all()
    return templates.TemplateResponse(
        "index.html", {"request": request, "articles": articles, "username": None}
    )


@app.get("/new", response_class=HTMLResponse)
async def add_article_form_endpoint(request: Request,credentials: Annotated[HTTPBasicCredentials, Depends(security)], title: str | None=None, date: str | None = None, content: str | None = None):
    if title and date and content:
        data = {
            "title": title,
            "content": content,
            "date": date,
            "author": credentials.username
        } 
        add_article(data)
    return templates.TemplateResponse(
        "add-article-form.html", {
            "request": request,
            "username": credentials.username,
        }
    )

@app.post("/new/add")
async def add_article_endpoint(request: Request,credentials: Annotated[HTTPBasicCredentials, Depends(security)], title: str = Form(...), date: str = Form(...), content: str = Form(...)):
    data = {
        "title": title,
        "content": content,
        "date": date,
        "author": credentials.username
    }



@app.get("/profile", response_class=HTMLResponse)
async def profile_endpoint(
    request: Request, credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    if credentials.username.lower() == "admin":
        return RedirectResponse(url="/admin")
    articles = get_all(credentials.username)

    return templates.TemplateResponse(
        "profile.html",
        {
            "request": request,
            "username": credentials.username,
            "articles": articles
        },
    )


@app.get("/admin", response_class=HTMLResponse)
async def admin_page_endpoint(
    request: Request, credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    articles = get_all()
    return templates.TemplateResponse("admin.html", {"request": request, "username": credentials.username, "articles": articles})


@app.get("/delete/{article_id}")
def delete_article_endpoint(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)], article_id: str
):
    delete_article(article_id)
    if credentials.username.lower() == "admin":
        return RedirectResponse(url="/admin")
    return RedirectResponse(url="/profile")

@app.get("/article/{article_id}")
async def get_one_article_endpoint(request: Request, article_id: str):
    article = get_by_id(article_id)
    return templates.TemplateResponse("article.html", {"request": request, "article": article})


# TODO: LOGOUT
