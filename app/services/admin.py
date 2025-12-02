from app.database.database import get_conn
import app.services.system as system_svc
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

def promote_user(user_id: int):
    with get_conn() as c:
        c.execute("UPDATE users SET role_id = 1 WHERE id = ?", (user_id,))
        c.commit()

def demote_user(user_id: int):
    with get_conn() as c:
        c.execute("UPDATE users SET role_id = 0 WHERE id = ?", (user_id,))
        c.commit()

def delete_user(user_id: int):
    with get_conn() as c:
        file_paths = c.execute("""
            SELECT q.image_path
            FROM quizzes q
            WHERE q.user_id = ?
        """, (user_id,)).fetchall()

        i = 0
        for file_path in file_paths:
            system_svc.remove_file_from_db("app/" + file_path[i])
            i += 1

        c.execute("""
            DELETE FROM quizzes WHERE user_id = ?
        """,(user_id,))

        c.execute("DELETE FROM users WHERE id = ?", (user_id,))
        c.commit()