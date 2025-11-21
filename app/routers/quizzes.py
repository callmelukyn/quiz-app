import json
from http.client import responses

from fastapi import APIRouter, Request, Form, UploadFile, File, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import app.services.quizzes as quizzes_svc
import app.services.session as session_svc

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/create", response_class=HTMLResponse)
def get_quiz_form(request: Request, user=Depends(session_svc.get_current_user)):
    return templates.TemplateResponse("create_quiz.html", {
        "request": request,
        "questions": [],
        "user": user
    })

@router.post("/create", response_class=HTMLResponse)
async def post_quiz_form(
    request: Request,
    user=Depends(session_svc.get_current_user),
    data: str = Form(None),
    image: UploadFile = File(None)
):
    # ochrana prázdného JSONu
    if not data:
        return templates.TemplateResponse(
            "create_quiz.html",
            {"request": request, "questions": [], "user": user}
        )

    payload = json.loads(data)

    quiz_id = quizzes_svc.create_quiz(
        payload=payload,
        image=image,
        user_id=user["id"]
    )

    return templates.TemplateResponse(
        "quiz_created.html",
        {"request": request, "quiz_id": quiz_id, "user": user}
    )

@router.get("/", response_class=HTMLResponse)
def show_all_quizzes(request: Request, user=Depends(session_svc.get_current_user)):
    quizzes = quizzes_svc.get_all_quizzes()
    return templates.TemplateResponse(
        "all_quizzes.html", {"request": request, "quizzes": quizzes, "user": user}
    )

@router.get("/mine", response_class=HTMLResponse)
def show_mine_quizzes(request: Request, user=Depends(session_svc.get_current_user)):
    quizzes = quizzes_svc.get_mine_quizzes(user["id"])
    return templates.TemplateResponse("my_quizzes.html", {"request": request, "quizzes": quizzes, "user": user})

@router.get("/{quiz_id}", response_class=HTMLResponse)
def show_quiz(request: Request, quiz_id: int, user=Depends(session_svc.get_current_user)):
    #quiz card
    quiz = quizzes_svc.get_quiz(quiz_id)
    #stats
    user_id = user["id"]
    average_score = quizzes_svc.get_average_score(quiz_id)
    your_average_score = quizzes_svc.get_your_average_score(quiz_id, user_id)
    total_entries = quizzes_svc.get_number_of_entries(quiz_id)
    your_entries = quizzes_svc.get_number_of_your_entries(quiz_id,user_id)
    stats = (average_score, your_average_score, total_entries, your_entries)
    return templates.TemplateResponse(
        "quiz.html", {"request": request, "quiz": quiz, "stats": stats, "user": user})

@router.get("/delete/{quiz_id}", response_class=HTMLResponse)
def delete_quiz(request: Request, quiz_id: int, user=Depends(session_svc.get_current_user)):
    if quizzes_svc.delete_quiz(quiz_id, user["id"]):
        return templates.TemplateResponse("quiz_deleted.html", {"request": request, "user": user})
    else:
        return templates.TemplateResponse("quiz_deleted_failed.html", {"request": request, "user": user})

@router.get("/edit/{quiz_id}", response_class=HTMLResponse)
def edit_quiz(request: Request, quiz_id: int, user=Depends(session_svc.get_current_user)):
    quiz = quizzes_svc.get_quiz_full(quiz_id)
    return templates.TemplateResponse("edit_quiz.html", {"request": request, "quiz": quiz, "user": user})

@router.post("/edit/{quiz_id}", response_class=HTMLResponse)
async def edit_quiz_post(
    request: Request,
    quiz_id: int,
    user=Depends(session_svc.get_current_user),
    data: str = Form(None),
    image: UploadFile = File(None),
):
    payload = json.loads(data)
    quizzes_svc.update_quiz(quiz_id, payload, image)
    return templates.TemplateResponse("quiz_updated.html", {"request": request,"quiz_id": quiz_id,"user": user})


