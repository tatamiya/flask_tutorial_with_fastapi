from typing import Optional

from fastapi import APIRouter, Request, Form, status, Cookie, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/auth", tags=["auth"])

templates = Jinja2Templates(directory="fastapir/templates")

fake_users_db = {1: {"username": "test_user", "hashed_password": "test_password"}}


async def load_logged_in_user(user_id: Optional[int] = Cookie(None)):
    if user_id:
        user = fake_users_db.get(user_id)
        if user:
            return user.get("username")
    return None


async def login_required(user_id: Optional[int] = Cookie(None)):
    if not user_id:
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)


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

    for user_id, user in fake_users_db.items():
        if username == user["username"] and password == user["hashed_password"]:
            response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
            response.set_cookie(key="user_id", value=user_id)
            return response

    raise HTTPException(status_code=400, detail="Inactive user")


@router.get("/logout/", response_class=RedirectResponse)
async def logout():
    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("user_id")
    return response
