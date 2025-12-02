from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from app.services import admin as admin_svc
from app.services import session as session_svc
router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def show_admin_dash(request: Request, user=Depends(session_svc.get_current_user)):
    if user["role"] == "admin":
        return templates.TemplateResponse(
            "admin.html", {"request": request, "user": user}
        )
    else:
        return RedirectResponse("/dashboard", status_code=302)
@router.get("/search-users")
def search_users(q: str = ""):
    rows = admin_svc.search_users(q)
    return [dict(row) for row in rows]

@router.post("/edit-points/{user_id}")
def update_points(user_id: int, score: dict):
    if "score" not in score:
        raise HTTPException(status_code=400, detail="Score value is missing")
    raw_val = score["score"]
    try:
        score_val = int(raw_val)
    except (ValueError, TypeError):
        raise HTTPException(status_code=400, detail="Entered score value is invalid")

    if score_val < 0:
        raise HTTPException(status_code=400, detail="Score cannot be negative")

    admin_svc.edit_points(user_id, score_val)
    return {"status": "ok"}

@router.post("/promote-user/{user_id}")
def promote_user(user_id: int):
    admin_svc.promote_user(user_id)
    return {"status": "ok"}

@router.post("/demote-user/{user_id}")
def demote_user(user_id: int):
    admin_svc.demote_user(user_id)
    return {"status": "ok"}

@router.delete("/delete-user/{user_id}")
def remove_user(user_id: int):
    admin_svc.delete_user(user_id)
    return {"status": "deleted"}
