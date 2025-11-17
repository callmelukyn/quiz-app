import os

from app.database.database import get_conn

def add_points(player_id: int, added_points: int):
    with get_conn() as c:
        c.execute(
            """UPDATE users
                SET score = score +?
                WHERE id = ?
            """,(added_points, player_id)
        )
        c.commit()

def add_points_to_quiz_owner(quiz_id: int):
    with get_conn() as c:
        author = c.execute("""
            SELECT user_id as author_id
            FROM quizzes
            WHERE id = ?
        """,(quiz_id,)).fetchone()

        c.execute("""
            UPDATE users SET score = score + 10 WHERE id = ?
        """, (author['author_id'],))
        c.commit()
    print(f"Successfully added 10 points to user '{author['author_id']}'")

def remove_file_from_db(filename: str):
    print(f"Removing {filename}...")
    try: os.remove(filename)
    except FileNotFoundError: print(f"File '{filename}' not found.")
    print(f"File '{filename}' deleted successfully.")