from typing import Optional

from fastapi import APIRouter, Request, Form, status, Cookie, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .db import crud
from .db.database import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/auth", tags=["auth"])

templates = Jinja2Templates(directory="fastapir/templates")


async def load_logged_in_user(
    user_id: Optional[int] = Cookie(None), db: Session = Depends(get_db)
):
    if user_id:
        user = crud.get_user_by_id(db, user_id)
        if user:
            return user.username
    return None


async def login_required(user_id: Optional[int] = Cookie(None)):
    if not user_id:
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hashed(password):
    return pwd_context.hash(password)


def authenticate_user(db: Session, username: str, password: str):
    user: crud.User = crud.get_user_by_name(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user.id


@router.get("/login/", response_class=HTMLResponse)
async def login(
    request: Request, username: Optional[str] = Depends(load_logged_in_user)
):
    if username:
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse(
        "login.html", {"request": request, "username": username}
    )


@router.post("/login/", response_class=RedirectResponse)
async def login_user_auth(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):

    user_id = authenticate_user(db, username, password)
    if user_id is None:
        raise HTTPException(status_code=400, detail="Inactive user")

    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="user_id", value=user_id)
    return response


@router.get("/register/", response_class=HTMLResponse)
async def register_page(
    request: Request, username: Optional[str] = Depends(load_logged_in_user)
):
    if username:
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register/", response_class=RedirectResponse)
async def register_user(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):

    user = crud.get_user_by_name(db, username)
    if user:
        raise HTTPException(status_code=400, detail="Already registered")

    hashed_password = get_password_hashed(password)
    new_user = crud.UserCreate(username=username, hashed_password=hashed_password)
    created_user = crud.create_user(db, new_user)

    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="user_id", value=created_user.id)
    return response


@router.get("/logout/", response_class=RedirectResponse)
async def logout():
    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("user_id")
    return response
