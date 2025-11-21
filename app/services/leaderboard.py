from app.database.database import get_conn


def get_leaderboard():
    with get_conn() as c:
        rows = c.execute(
            "SELECT id, nickname, score FROM users WHERE score > 0 ORDER BY score DESC"
        ).fetchmany(100)
        return rows