from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse
from app.database.database import get_conn


def get_current_user(request: Request):
    session_code = request.cookies.get("session")
    if not session_code:
        raise HTTPException(status_code=303, detail="Redirect", headers={"Location": "/auth/login"})

    with get_conn() as c:
        user_id = c.execute("""
            SELECT user_id
            FROM sessions
            WHERE session_code = ?
        """, (session_code,)).fetchone() #podle sessionu si zjistim id usera a toho vratim

        user = c.execute(
            """
            SELECT users.id, users.nickname, roles.name as role, users.score
            FROM users
            JOIN roles ON users.role_id = roles.id
            WHERE users.id = ?
            """,
            (user_id["user_id"],)
        ).fetchone()

    if not user:
        response = RedirectResponse("/auth/login")
        response.delete_cookie("session", path="/")
        raise HTTPException(status_code=303, detail="Redirect", headers={"Location": "/auth/login"})
    return user
