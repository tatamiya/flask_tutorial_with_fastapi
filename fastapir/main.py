from typing import Optional

from fastapi import FastAPI, Request, Cookie
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from . import auth

app = FastAPI()

app.mount("/static", StaticFiles(directory="fastapir/static"), name="static")

templates = Jinja2Templates(directory="fastapir/templates")

app.include_router(auth.router)


@app.get("/hello")
def hello():
    return "Hello, World!"


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, username: Optional[str] = Cookie(None)):
    return templates.TemplateResponse(
        "index.html", {"request": request, "username": username}
    )
