import json
from fastapi import APIRouter, Request, Form, UploadFile, File, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

import app.services.quizzes as quizzes_svc
import app.services.session as session_svc

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
        user_id=6        # TODO: vzít z tokenu
    )

    return templates.TemplateResponse(
        "quiz_created.html",
        {"request": request, "quiz_id": quiz_id}
    )

@router.get("/", response_class=HTMLResponse)
def show_all_quizzes(request: Request, user=Depends(session_svc.get_current_user)):
    quizzes = quizzes_svc.get_all_quizzes()
    return templates.TemplateResponse(
        "all_quizzes.html", {"request": request, "quizzes": quizzes, "user": user}
    )

@router.get("/mine", response_class=HTMLResponse)
def show_mine_quizzes(request: Request, user=Depends(session_svc.get_current_user)):
    if not user:
        return RedirectResponse("/auth/login")
    quizzes = quizzes_svc.get_mine_quizzes(1)    #TODO service pro získání kvízu pouze uživatele
    return templates.TemplateResponse("my_quizzes.html", {"request": request, "quizzes": quizzes, "user": user})
#TODO Z tokenu zjistit ID uzivatele a dat do funkce

@router.get("/{quiz_id}", response_class=HTMLResponse)
def show_quiz(request: Request, quiz_id: int):
    #quiz card
    quiz = quizzes_svc.get_quiz(quiz_id)
    #stats
    average_score = quizzes_svc.get_average_score(quiz_id)
    your_average_score = quizzes_svc.get_your_average_score(quiz_id, 2)
    total_entries = quizzes_svc.get_number_of_entries(quiz_id)
    your_entries = quizzes_svc.get_number_of_your_entries(quiz_id,2) #TODO fixnout na token
    stats = (average_score, your_average_score, total_entries, your_entries)
    return templates.TemplateResponse(
        "quiz.html", {"request": request, "quiz": quiz, "stats": stats}
    )



