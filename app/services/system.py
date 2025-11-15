import os

from app.database.database import get_conn

def add_points(player_id: int, added_points: int):
    with get_conn() as c:
        rows = c.execute(
            """UPDATE users
            SET score = """
        )
        return rows

def remove_file_from_db(filename: str):
    print(f"Removing {filename}...")
    try: os.remove(filename)
    except FileNotFoundError: print(f"File '{filename}' not found.")
    print(f"File '{filename}' deleted successfully.")