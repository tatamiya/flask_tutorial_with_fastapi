from typing import Optional

from fastapi import APIRouter, Request, Form, status, Cookie, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext

from .db import fake_users_db

router = APIRouter(prefix="/auth", tags=["auth"])

templates = Jinja2Templates(directory="fastapir/templates")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
    for user_id, user in db.items():
        if username == user["username"]:
            return user_id, user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db, username: str, password: str):
    user_id, user = get_user(db, username)
    if not user:
        return None
    if not verify_password(password, user.get("hashed_password")):
        return None
    return user_id


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


@router.get("/logout/", response_class=RedirectResponse)
async def logout():
    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("user_id")
    return response
