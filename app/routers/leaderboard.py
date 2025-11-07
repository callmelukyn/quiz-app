from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services import leaderboard

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def show_leaderboard(request: Request):
    data = leaderboard.get_leaderboard()
    return templates.TemplateResponse(
        "leaderboard.html", {"request": request, "players": data}
    )
