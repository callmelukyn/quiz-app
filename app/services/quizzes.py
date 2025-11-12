from app.database.database import get_conn


def get_all_quizzes():
    with get_conn() as c:
        rows = c.execute(
            """
            SELECT
                q.image_path,
                q.title,
                q.description,
                u.nickname,
                q.id
            FROM quizzes q
            JOIN users u ON q.user_id = u.id;
            """
        ).fetchall()
        return rows

def get_quiz(id: int):
    with get_conn() as c:
        rows = c.execute(
            """
            SELECT
                q.image_path,
                q.title,
                q.description,
                u.nickname,
                q.id
            FROM quizzes q
            JOIN users u ON q.user_id = u.id
            WHERE q.id = ?;
            """,(id,)
        ).fetchall()
        return rows

def get_mine_quizzes(id: int):
    with get_conn() as c:
        rows = c.execute(
            """
            SELECT
                q.image_path,
                q.title,
                q.description,
                u.nickname,
                q.id
            FROM quizzes q
            JOIN users u ON q.user_id = u.id
            WHERE u.id = ?;
            """,id
        ).fetchall()
        return rows