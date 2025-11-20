from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse
from app.database.database import get_conn


def get_current_user(request: Request):
    user_id = request.cookies.get("session")
    if not user_id:
        raise HTTPException(status_code=303, detail="Redirect", headers={"Location": "/auth/login"})

    with get_conn() as c:
        user = c.execute(
            """
            SELECT users.id, users.nickname, roles.name as role, users.score
            FROM users
            JOIN roles ON users.role_id = roles.id
            WHERE users.id = ?
            """,
            (user_id,)
        ).fetchone()

    if not user:
        response = RedirectResponse("/auth/login")
        response.delete_cookie("session", path="/")
        raise HTTPException(status_code=303, detail="Redirect", headers={"Location": "/auth/login"})
    return user
