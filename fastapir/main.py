from typing import Optional

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware

from fastapir.config import Settings
from fastapir.db import crud
from fastapir.db.database import Base, engine, get_db

from . import auth, blog

# Setup tables if no exists
# This must be here.
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="fastapir/static"), name="static")

templates = Jinja2Templates(directory="fastapir/templates")

app.include_router(auth.router)
app.include_router(blog.router)

app.add_middleware(
    SessionMiddleware,
    secret_key=Settings().session_secret_key,
    max_age=15 * 60,
)


@app.get("/hello")
def hello():
    return "Hello, World!"


@app.get("/", response_class=HTMLResponse)
async def index(
    request: Request,
    user: Optional[auth.LoggedInUser] = Depends(auth.load_logged_in_user),
    db: Session = Depends(get_db),
):
    posts = crud.get_posts(db)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "user": user, "posts": posts},
    )
