import datetime
from typing import Optional

from fastapi import APIRouter, Request, Form, status, Cookie, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from fastapir.auth import load_logged_in_user
from fastapir.db import crud
from fastapir.db.database import get_db

router = APIRouter(prefix="/blog", tags=["blog"])
templates = Jinja2Templates(directory="fastapir/templates")


@router.get("/create/", response_class=HTMLResponse)
async def create_page(
    request: Request, username: Optional[str] = Depends(load_logged_in_user)
):
    if not username:
        return RedirectResponse("/auth/login", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse(
        "create.html", {"request": request, "username": username}
    )


@router.post("/create/", response_class=RedirectResponse)
async def register_user(
    title: str = Form(...),
    body: str = Form(...),
    username: Optional[str] = Depends(load_logged_in_user),
    user_id: Optional[int] = Cookie(None),
    db: Session = Depends(get_db),
):
    if not username:
        raise HTTPException(status_code=401, detail="Invalid Authentication")

    created_at = datetime.datetime.now()
    new_post = crud.PostCreate(
        title=title,
        body=body,
        author_id=user_id,
        created_at=created_at,
    )
    crud.create_post(db, new_post)

    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    return response
