import json
from fastapi import APIRouter, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import app.services.quizzes as quizzes_svc

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/create", response_class=HTMLResponse)
def get_quiz_form(request: Request):
    return templates.TemplateResponse("create_quiz.html", {
        "request": request,
        "questions": []
    })

@router.post("/create", response_class=HTMLResponse)
async def post_quiz_form(
    request: Request,
    data: str = Form(None),
    image: UploadFile = File(None)
):
    # ochrana prázdného JSONu
    if not data:
        return templates.TemplateResponse(
            "create_quiz.html",
            {"request": request, "questions": []}
        )

    payload = json.loads(data)

    quiz_id = quizzes_svc.create_quiz(
        payload=payload,
        image=image,
        user_id=11        # TODO: vzít z tokenu
    )

    return templates.TemplateResponse(
        "quiz_created.html",
        {"request": request, "quiz_id": quiz_id}
    )

@router.get("/", response_class=HTMLResponse)
def show_all_quizzes(request: Request):
    quizzes = quizzes_svc.get_all_quizzes()
    return templates.TemplateResponse(
        "all_quizzes.html", {"request": request, "quizzes": quizzes}
    )

@router.get("/mine", response_class=HTMLResponse)
def show_all_quizzes(request: Request):
    user_id: int = 1
    quizzes = quizzes_svc.get_mine_quizzes(user_id)    #TODO service pro získání kvízu pouze uživatele
    return templates.TemplateResponse(
        "my_quizzes.html", {"request": request, "quizzes": quizzes}
    )
#TODO Z tokenu zjistit ID uzivatele a dat do funkce

@router.get("/{id}", response_class=HTMLResponse)
def show_quiz(request: Request, id: int):
    quiz = quizzes_svc.get_quiz(id)
    return templates.TemplateResponse(
        "quiz.html", {"request": request, "quiz": quiz}
    )



