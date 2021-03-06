import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from fastapir.auth import LoggedInUser, load_logged_in_user
from fastapir.db import crud, models
from fastapir.db.database import get_db

router = APIRouter(prefix="/blog", tags=["blog"])
templates = Jinja2Templates(directory="fastapir/templates")


@router.get("/create/", response_class=HTMLResponse)
async def create_page(
    request: Request, user: Optional[LoggedInUser] = Depends(load_logged_in_user)
):
    if not user:
        return RedirectResponse("/auth/login", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse(
        "blog/create.html",
        {
            "request": request,
            "user": user,
            "title_maxlength": models.MAX_BLOG_TITLE_LENGTH,
            "body_maxlength": models.MAX_BLOG_BODY_LENTGH,
        },
    )


@router.post("/create/", response_class=RedirectResponse)
async def create_post(
    title: str = Form(..., max_length=models.MAX_BLOG_TITLE_LENGTH),
    body: str = Form(..., max_length=models.MAX_BLOG_BODY_LENTGH),
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

    if post is None:
        raise HTTPException(status_code=404, detail="Resource Not Found")
    if post.author_id != user.user_id:
        raise HTTPException(status_code=401, detail="Invalid Authentication")

    return templates.TemplateResponse(
        "blog/update.html",
        {
            "request": request,
            "user": user,
            "post": post,
            "title_maxlength": models.MAX_BLOG_TITLE_LENGTH,
            "body_maxlength": models.MAX_BLOG_BODY_LENTGH,
        },
    )


@router.post("/{id}/update", response_class=RedirectResponse)
async def update_post(
    id: int,
    title: str = Form(..., max_length=models.MAX_BLOG_TITLE_LENGTH),
    body: str = Form(..., max_length=models.MAX_BLOG_BODY_LENTGH),
    user: Optional[LoggedInUser] = Depends(load_logged_in_user),
    db: Session = Depends(get_db),
):
    if not user:
        raise HTTPException(status_code=401, detail="Invalid Authentication")

    post_to_update = crud.PostUpdate(
        id=id,
        title=title,
        body=body,
        author_id=user.user_id,
    )
    try:
        crud.update_post(db, post_to_update)
    except crud.NotFoundError:
        raise HTTPException(status_code=404, detail="Resource Not Found")
    except crud.AuthenticationError:
        raise HTTPException(status_code=401, detail="Invalid Authentication")

    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    return response


@router.post("/{id}/delete", response_class=RedirectResponse)
async def delete_post(
    id: int,
    user: Optional[LoggedInUser] = Depends(load_logged_in_user),
    db: Session = Depends(get_db),
):
    if not user:
        raise HTTPException(status_code=401, detail="Invalid Authentication")

    post_to_delete = crud.PostDelete(
        id=id,
        author_id=user.user_id,
    )
    try:
        crud.delete_post(db, post_to_delete)
    except crud.NotFoundError:
        raise HTTPException(status_code=404, detail="Resource Not Found")
    except crud.AuthenticationError:
        raise HTTPException(status_code=401, detail="Invalid Authentication")

    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    return response
