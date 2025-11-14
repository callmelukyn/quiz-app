from app.database.database import get_conn

def edit_points(user_id: int, new_points: int):
    with get_conn() as c:
        c.execute(
            """UPDATE users
                SET score = ?
                WHERE id = ?""",
            (new_points, user_id)
        )
        c.commit()

def search_users(q: str = ""):
    with get_conn() as c:
        rows = c.execute("""
            SELECT u.id, u.nickname, u.email, u.score, r.name as role
            FROM users u
            JOIN roles r ON u.role_id = r.id
            WHERE nickname LIKE '%' || ? || '%'
            ORDER BY nickname ASC
            LIMIT 20;
        """, (q,)).fetchall()
    return rows

def delete_user(user_id: int):
    with get_conn() as c:
        c.execute("DELETE FROM users WHERE id = ?", (user_id,))
        c.commit()