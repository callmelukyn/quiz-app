from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.routers import leaderboard, aboutus, auth, dashboard

app = FastAPI(title="Quizzer")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/quiz_img", StaticFiles(directory="app/database/quiz_img"), name="quiz_img")
templates = Jinja2Templates(directory="app/templates")

# Routy
app.include_router(leaderboard.router, prefix="/leaderboard", tags=["leaderboard"])
app.include_router(aboutus.router, prefix="/aboutus", tags=["aboutus"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])

@app.get("/")
def landing(request: Request):
    return templates.TemplateResponse("landing.html", {"request": request})
