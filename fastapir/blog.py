from typing import Optional

from fastapi import APIRouter, Request, Form, status, Cookie, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.orm import Session

from fastapir.auth import load_logged_in_user

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
