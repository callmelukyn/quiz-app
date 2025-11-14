from app.database.database import get_conn

def get_player_statistics(id: int):
    with get_conn() as c:
        rows = c.execute(
            """SELECT u.nickname, u.score, p.placement, r.name
               FROM users u
               JOIN roles r ON u.role_id = r.id
               JOIN (
                    SELECT id, RANK() OVER (ORDER BY score DESC) AS placement
                    FROM users
               ) AS p ON p.id = u.id
                WHERE u.id = ?
            """, (id,)).fetchone()
        return rows