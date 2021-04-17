import datetime
from typing import Optional

from fastapi import APIRouter, Request, Form, status, Cookie, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from fastapir.auth import load_logged_in_user, LoggedInUser
from fastapir.db import crud
from fastapir.db.database import get_db

router = APIRouter(prefix="/blog", tags=["blog"])
templates = Jinja2Templates(directory="fastapir/templates")


@router.get("/create/", response_class=HTMLResponse)
async def create_page(
    request: Request, user: Optional[LoggedInUser] = Depends(load_logged_in_user)
):
    if not user:
        return RedirectResponse("/auth/login", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("create.html", {"request": request, "user": user})


@router.post("/create/", response_class=RedirectResponse)
async def create_post(
    title: str = Form(...),
    body: str = Form(...),
    user: Optional[LoggedInUser] = Depends(load_logged_in_user),
    db: Session = Depends(get_db),
):
    if not user:
        raise HTTPException(status_code=401, detail="Invalid Authentication")

    created_at = datetime.datetime.now()
    new_post = crud.PostCreate(
        title=title,
        body=body,
        author_id=user.user_id,
        created_at=created_at,
    )
    crud.create_post(db, new_post)

    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    return response


@router.get("/{id}/update", response_class=HTMLResponse)
async def update_page(
    id: int,
    request: Request,
    user: Optional[LoggedInUser] = Depends(load_logged_in_user),
    db: Session = Depends(get_db),
):
    if not user:
        return RedirectResponse("/auth/login", status_code=status.HTTP_302_FOUND)

    post = crud.get_post(db, id)
    if post.author_id != user.user_id:
        raise HTTPException(status_code=401, detail="Invalid Authentication")

    return templates.TemplateResponse(
        "update.html", {"request": request, "user": user, "post": post}
    )
