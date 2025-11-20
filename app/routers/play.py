from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services import play as play_svc
from app.services import system as system_svc
import app.services.session as session_svc

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/{id}", response_class=HTMLResponse)
def play_quiz(request: Request, id: int, user=Depends(session_svc.get_current_user)):
    quiz = play_svc.get_quiz_full(id)
    return templates.TemplateResponse(
        "play_quiz.html",
        {"request": request, "quiz": quiz, "user": user}
    )

@router.post("/{id}", response_class=HTMLResponse)
async def evaluate_quiz(request: Request, id: int, user=Depends(session_svc.get_current_user)):
    form = await request.form()
    quiz = play_svc.get_quiz_full(id)

    correct_count = 0
    total = len(quiz["questions"])

    for q in quiz["questions"]:
        submitted = form.get(f"q_{q['id']}")
        for ans in q["answers"]:
            if ans["is_correct"] == 1 and str(ans["id"]) == submitted:
                correct_count += 1

    score_percent = int((correct_count / total) * 100)

    user_id = user["id"]
    play_svc.log_quiz_attempt(id, user_id, score_percent)
    user_eligible = play_svc.is_user_eligible_to_get_points(id, user_id)
    if user_eligible:
        system_svc.add_points(user_id, 100)
        system_svc.add_points_to_quiz_owner(id)
        print(f"User is eligible, giving 100 points to ID: {user_id} and 10 points to quiz author")
    return templates.TemplateResponse(
        "quiz_result.html",
        {
            "request": request,
            "user": user,
            "quiz": quiz,
            "correct": correct_count,
            "total": total,
            "percent": score_percent,
            "user_eligible": user_eligible
        }
    )