from app.database.database import get_conn

def add_points(player_id: int, added_points: int):
    with get_conn() as c:
        rows = c.execute(
            """UPDATE users
            SET score = """
        )
        return rows