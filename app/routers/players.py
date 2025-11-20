from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services import players as players_svc

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/{id}", response_class=HTMLResponse)
def show_player_stats(request: Request, id: int):
    player = players_svc.get_player_statistics(id)
    quiz_stats = players_svc.get_quiz_statistics(id)
    return templates.TemplateResponse(
        "players.html", {"request": request, "player": player, "quiz_stats": quiz_stats}
    )