from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.routers import landing, leaderboard, aboutus, auth, dashboard, quizzes, players, admin, play

app = FastAPI(title="Quizzer")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/quiz_img", StaticFiles(directory="app/database/quiz_img"), name="quiz_img")
templates = Jinja2Templates(directory="app/templates")

# Routy
app.include_router(landing.router, tags=["landing"])
app.include_router(leaderboard.router, prefix="/leaderboard", tags=["leaderboard"])
app.include_router(aboutus.router, prefix="/aboutus", tags=["aboutus"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
app.include_router(quizzes.router, prefix="/quizzes", tags=["quizzes"])
app.include_router(players.router, prefix="/players", tags=["players"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(play.router, prefix="/play", tags=["play"])
