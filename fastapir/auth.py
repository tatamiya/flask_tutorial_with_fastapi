from typing import Optional

from fastapi import APIRouter, Request, Form, status, Cookie, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from passlib.context import CryptContext

from .db import fake_users_db

router = APIRouter(prefix="/auth", tags=["auth"])

templates = Jinja2Templates(directory="fastapir/templates")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseModel):
    user_id: int
    username: str
    hashed_password: str


async def load_logged_in_user(user_id: Optional[int] = Cookie(None)):
    if user_id:
        user = fake_users_db.get(user_id)
        if user:
            return user.get("username")
    return None


async def login_required(user_id: Optional[int] = Cookie(None)):
    if not user_id:
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)


def get_user(db, username: str):
    for user_id, user_in_db in db.items():
        if username == user_in_db["username"]:
            user = User(user_id=user_id, **user_in_db)
            return user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hashed(password):
    return pwd_context.hash(password)


def authenticate_user(db, username: str, password: str):
    user: User = get_user(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user.user_id


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
async def login_user_auth(username: str = Form(...), password: str = Form(...)):

    user_id = authenticate_user(fake_users_db, username, password)
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
async def register_user(username: str = Form(...), password: str = Form(...)):

    user = get_user(fake_users_db, username)
    if user:
        raise HTTPException(status_code=400, detail="Already registered")

    new_user_id = max(fake_users_db.keys()) + 1
    hashed_password = get_password_hashed(password)
    fake_users_db[new_user_id] = {
        "username": username,
        "hashed_password": hashed_password,
    }

    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="user_id", value=new_user_id)
    return response


@router.get("/logout/", response_class=RedirectResponse)
async def logout():
    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("user_id")
    return response
