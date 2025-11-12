from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import app.services.quizzes as sc_quizzes

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def show_all_quizzes(request: Request):
    quizzes = sc_quizzes.get_all_quizzes()
    return templates.TemplateResponse(
        "all_quizzes.html", {"request": request, "quizzes": quizzes}
    )

@router.get("/{id}", response_class=HTMLResponse)
def show_quiz(request: Request, id: int):
    quiz = sc_quizzes.get_quiz(id)
    return templates.TemplateResponse(
        "quiz.html", {"request": request, "quiz": quiz}
    )

@router.get("/mine", response_class=HTMLResponse)
def show_all_quizzes(request: Request):
    user_id: int = 2
    my_quizzes = sc_quizzes.get_mine_quizzes(user_id)    #TODO service pro získání kvízu pouze uživatele
    return templates.TemplateResponse(
        "my_quizzes.html", {"request": request, "quizzes": my_quizzes}
    )
#TODO Z tokenu zjistit ID uzivatele a dat do funkce