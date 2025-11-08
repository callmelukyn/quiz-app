from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

import app.services.auth as auth

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login", response_class=HTMLResponse)
def login_form_post(email: str = Form(...), password: str = Form(...)):
    if auth.login(email, password) == True:
        return HTMLResponse(content="Successfully logged in")
    else:
        return HTMLResponse(content="Failed to log in!")

@router.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register", response_class=HTMLResponse)
def register_form_post(email: str = Form(...), name: str = Form(...), password: str = Form(...)):
    auth.register(email, name, password)
    return RedirectResponse(url="/auth/login", status_code=303)