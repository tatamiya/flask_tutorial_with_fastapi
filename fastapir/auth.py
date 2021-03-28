from typing import Optional

from fastapi import APIRouter, Request, Form, status, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/auth", tags=["auth"])

templates = Jinja2Templates(directory="fastapir/templates")


async def login_required(username: Optional[str] = Cookie(None)):
    if not username:
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)


@router.get("/login/", response_class=HTMLResponse)
async def login(request: Request, username: Optional[str] = Cookie(None)):
    if username:
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse(
        "login.html", {"request": request, "username": username}
    )


@router.post("/login/", response_class=RedirectResponse)
async def login_user_auth(username: str = Form(...)):
    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="username", value=username)
    response.set_cookie(key="user_id", value=1)
    return response


@router.get("/logout/", response_class=RedirectResponse)
async def logout():
    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("username")
    response.delete_cookie("user_id")
    return response
