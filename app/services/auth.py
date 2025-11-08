from app.database.database import get_conn


def register(email, nickname, password):
    with get_conn() as c:
        c.execute(
            """INSERT OR IGNORE INTO users (email, nickname, password_hash) VALUES (?, ?, ?)"""
            ,(email, nickname, password)
        )
        c.commit()

def login(email, password):
    with get_conn() as c:
        r = c.execute(
            """
            SELECT * FROM users WHERE email = ? and password_hash = ?
            """, (email, password)
        ).fetchall()

        if (len(r) == 1):
            return True
        else:
            return False