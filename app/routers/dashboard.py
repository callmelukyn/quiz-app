from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

import app.services.session as session_svc
import app.services.auth as auth_svc

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def show_dashboard(request: Request, user=Depends(session_svc.get_current_user)):
    response = templates.TemplateResponse(
        "dashboard.html", {"request": request, "user": user}
    )
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@router.get("/logout")
def logout(request: Request, user=Depends(session_svc.get_current_user)):
    auth_svc.remove_session(user["id"])
    response = RedirectResponse("/auth/login", status_code=302)
    response.delete_cookie(
        "session",
        path="/",
        samesite="lax",
        secure = False
    )
    return response