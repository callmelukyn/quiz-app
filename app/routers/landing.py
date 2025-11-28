from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

import app.services.landing as landing_svc

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
def landing(request: Request):
    stats = (
        landing_svc.get_num_registered_users(),
        landing_svc.get_num_quizzes_created(),
        landing_svc.get_num_points_collected()
    )
    return templates.TemplateResponse("landing.html", {"request": request, "stats": stats})