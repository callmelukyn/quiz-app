from app.database.database import get_conn

def get_num_registered_users():
    with get_conn() as c:
        num = c.execute("""
            SELECT COUNT(DISTINCT(id)) as count
            FROM users
        """).fetchone()
    return num["count"]

def get_num_quizzes_created():
    with get_conn() as c:
        num = c.execute("""
            SELECT COUNT(DISTINCT(id)) as count
            FROM quizzes
        """).fetchone()
    return num["count"]

def get_num_points_collected():
    with get_conn() as c:
        num = c.execute("""
            SELECT SUM(score) as count
            FROM users
        """).fetchone()
    return num["count"]
