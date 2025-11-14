from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services import admin as admin_svc
router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def show_admin_dash(request: Request):
    return templates.TemplateResponse(
        "admin.html", {"request": request}
    )
@router.get("/search-users")
def search_users(q: str = ""):
    rows = admin_svc.search_users(q)
    return [dict(row) for row in rows]

@router.post("/edit-points/{user_id}")
def update_points(user_id: int, score: dict):
    admin_svc.edit_points(user_id, int(score["score"]))
    return {"status": "ok"}

@router.delete("/delete-user/{user_id}")
def remove_user(user_id: int):
    admin_svc.delete_user(user_id)
    return {"status": "deleted"}
