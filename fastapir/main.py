from typing import Optional

from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from fastapir.db import crud
from fastapir.db.database import get_db, Base, engine

from . import auth, blog

# Setup tables if no exists
# This must be here.
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="fastapir/static"), name="static")

templates = Jinja2Templates(directory="fastapir/templates")

app.include_router(auth.router)
app.include_router(blog.router)


@app.get("/hello")
def hello():
    return "Hello, World!"


@app.get("/", response_class=HTMLResponse)
async def index(
    request: Request,
    username: Optional[str] = Depends(auth.load_logged_in_user),
    db: Session = Depends(get_db),
):
    posts = crud.get_posts(db)
    return templates.TemplateResponse(
        "index.html", {"request": request, "username": username, "posts": posts}
    )
