from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services import play as play_svc
from app.services import system as system_svc

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/{id}", response_class=HTMLResponse)
def play_quiz(request: Request, id: int):
    quiz = play_svc.get_quiz_full(id)
    return templates.TemplateResponse(
        "play_quiz.html",
        {"request": request, "quiz": quiz}
    )

@router.post("/{id}", response_class=HTMLResponse)
async def evaluate_quiz(request: Request, id: int):
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

    user_id = 2 #TODO fixnout na token, aktualni hrac je ID 2
    play_svc.log_quiz_attempt(id, user_id, score_percent)
    user_eligible = play_svc.is_user_eligible_to_get_points(id, user_id)
    if user_eligible:
        system_svc.add_points(user_id, 100) #TODO 100 Bodu za 100% na kvizu, one-time, mozna fixnu
        system_svc.add_points_to_quiz_owner(id) #TODO Ve funkci je 10 bodu za splneni kvizu pro ownera
    print(user_eligible)
    return templates.TemplateResponse(
        "quiz_result.html",
        {
            "request": request,
            "quiz": quiz,
            "correct": correct_count,
            "total": total,
            "percent": score_percent,
            "user_eligible": user_eligible
        }
    )