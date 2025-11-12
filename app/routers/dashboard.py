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