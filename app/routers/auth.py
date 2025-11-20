
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

import app.services.auth as auth

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "data": ("", ""), "errors": []})

@router.post("/login")
def login_form_post(request: Request, email: str = Form(...), password: str = Form(...)):
    errors = auth.login_check(email,password)
    if errors:
        return templates.TemplateResponse("login.html", {"request": request, "data": (email, password), "errors": errors})

    user_id = auth.get_user_id_by_email(email)
    response = RedirectResponse("/dashboard", status_code=302)
    response.set_cookie(
        key="session",
        value=str(user_id),
        httponly=True,
        samesite="lax",
        path="/",
        max_age=60 * 60 * 24
    )
    return response


@router.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "data": ("", ""), "errors": []})

@router.post("/register")
def register_form_post(request: Request, email: str = Form(...), name: str = Form(...), password: str = Form(...)):
    errors = auth.register_check_availability(email,name)
    if errors:
        return templates.TemplateResponse("register.html", {"request": request, "errors": errors, "data": (email, name)})

    hashed_password = auth.hash_password(password)
    auth.register(email,name,hashed_password)
    user_id = auth.get_user_id_by_email(email)
    response = RedirectResponse("/dashboard", status_code=302)
    response.set_cookie(
        key="session",
        value=str(user_id),
        httponly=True,
        samesite="lax",
        path="/",
        max_age=60 * 60 * 24
    )
    return response