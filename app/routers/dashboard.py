from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import app.services.dashboard as dashboard

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def show_dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html", {"request": request}
    )

@router.get("/quizzes", response_class=HTMLResponse)
def show_all_quizzes(request: Request):
    quizzes = dashboard.get_all_quizzes()
    return templates.TemplateResponse(
        "all_quizzes.html", {"request": request, "quizzes": quizzes}
    )

@router.get("/my_quizzes", response_class=HTMLResponse)
def show_all_quizzes(request: Request):
    my_quizzes = dashboard.get_all_quizzes()    #TODO service pro získání kvízu pouze uživatele
    return templates.TemplateResponse(
        "my_quizzes.html", {"request": request, "quizzes": my_quizzes}
    )
