import bcrypt
import secrets
from app.database.database import get_conn


def register(email, nickname, hashed_password):
    with get_conn() as c:
        c.execute(
            """INSERT OR IGNORE INTO users (email, nickname, password_hash) VALUES (?, ?, ?)"""
            ,(email, nickname, hashed_password)
        )
        c.commit()

def register_check_availability(email, nickname):
    with get_conn() as c:
        errors = []
        email_row = c.execute(
            "SELECT email FROM users WHERE email = ?", (email,)
        ).fetchone()
        if email_row:
            errors.append(f'Email {email_row["email"]} is already registered')

        nick_row = c.execute(
            "SELECT nickname FROM users WHERE nickname = ?", (nickname,)
        ).fetchone()
        if nick_row:
            errors.append(f'Nickname {nick_row["nickname"]} is already in use')

    return errors

def login_check(email, password):
    with get_conn() as c:
        user = c.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()

        if not user:
            return ["Email is not registered"]

        if not bcrypt.checkpw(password.encode("utf-8"), user["password_hash"]):
            return ["Incorrect password"]

    return []

def hash_password(password):
    pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return pw


def get_user_hashed_password(email):
    with get_conn() as c:
        r = c.execute("SELECT password_hash FROM users WHERE email = ?", (email,)).fetchone()
    return r["password_hash"]

def get_user_id_by_email(email):
    with get_conn() as c:
        r = c.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
        return r["id"]

def get_and_insert_session(user_id: int):
    session_code = make_token()
    with get_conn() as c:
        c.execute("""
            INSERT INTO sessions (user_id, session_code) VALUES (?, ?)
        """, (user_id, session_code))
        c.commit()
    return session_code

def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)

def remove_session(user_id: int):
    with get_conn() as c:
        c.execute("DELETE FROM sessions WHERE user_id = ?", (user_id,))
        c.commit()

def make_token():
    return secrets.token_urlsafe(16)