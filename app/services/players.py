from app.database.database import get_conn

def get_player_statistics(user_id: int):
    with get_conn() as c:
        player = c.execute(
            """SELECT u.nickname, u.score, p.placement, r.name
               FROM users u
               JOIN roles r ON u.role_id = r.id
               JOIN (
                    SELECT id, RANK() OVER (ORDER BY score DESC) AS placement
                    FROM users
               ) AS p ON p.id = u.id
                WHERE u.id = ?
            """, (user_id,)).fetchone()

        active = c.execute("""
            SELECT COUNT(*)
            FROM sessions
            WHERE user_id = ?
        """, (user_id,)).fetchone()

        return (player[0], player[1], player[2], player[3], active[0])

def get_quiz_statistics(user_id: int):
    with get_conn() as c:
        quizzes_created = c.execute(
            """SELECT COUNT(*) as count
               FROM quizzes q
               WHERE q.user_id = ?
            """, (user_id,)).fetchone()

        obtained_by_others = c.execute(
            """SELECT COUNT(*) * 10 AS total_points
               FROM (
                    SELECT DISTINCT qr.user_id
                    FROM quizzes q
                    JOIN quiz_results qr ON qr.quiz_id = q.id
                    WHERE q.user_id = ?
                      AND qr.score = 100
                      AND qr.user_id <> ?
                ) AS unique_first_wins;
            """, (user_id, user_id)).fetchone()

        return (quizzes_created["count"], obtained_by_others["total_points"])