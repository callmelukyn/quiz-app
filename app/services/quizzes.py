from fastapi import UploadFile

from app.database.database import get_conn
import json,uuid

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
            """,(id,)
        ).fetchall()
        return rows

def save_image(image: UploadFile | None):
    # Pokud není obrázek nebo je prázdné filename, dej default
    if not image or image.filename == "":
        return "database/quiz_img/default.png"

    filename = f"{uuid.uuid4()}_{image.filename}"
    save_path = f"app/database/quiz_img/{filename}"

    with open(save_path, "wb") as f:
        f.write(image.file.read())

    return f"database/quiz_img/{filename}"

def create_quiz(payload: dict, image: UploadFile | None, user_id: int = 1):
    title = payload["title"]
    desc = payload["description"]
    questions = payload["questions"]

    image_path = save_image(image)

    with get_conn() as c:
        cursor = c.execute(
            """
            INSERT INTO quizzes (title, description, image_path, user_id)
            VALUES (?, ?, ?, ?)
            """,
            (title, desc, image_path, user_id)
        )
        quiz_id = cursor.lastrowid

        # otázky
        for q in questions:
            qcur = c.execute(
                "INSERT INTO questions (quiz_id, text) VALUES (?, ?)",
                (quiz_id, q["text"])
            )
            question_id = qcur.lastrowid

            # odpovědi
            for ans in q["answers"]:
                c.execute(
                    """
                    INSERT INTO answers (question_id, text, is_correct)
                    VALUES (?, ?, ?)
                    """,
                    (question_id, ans["text"], ans["correct"])
                )
        c.commit()
    return quiz_id

def get_average_score(quiz_id: int):
    with get_conn() as c:
        row = c.execute("""
            SELECT COALESCE(AVG(score), 0) as average_score
            FROM quiz_results
            WHERE quiz_id = ?;
        """,(quiz_id,)).fetchone()
    return row["average_score"]

def get_your_average_score(quiz_id: int, user_id: int):
    with get_conn() as c:
        row = c.execute("""
            SELECT COALESCE(AVG(score), 0) as average_score
            FROM quiz_results
            WHERE quiz_id = ? AND user_id = ?;
        """,(quiz_id,user_id)).fetchone()
    return row["average_score"]


def get_number_of_entries(quiz_id: int):
    with get_conn() as c:
        row = c.execute("""
            SELECT COUNT(*) as count
            FROM quiz_results
            WHERE quiz_id = ?;
        """,(quiz_id,)).fetchone()
    return row["count"]

def get_number_of_your_entries(quiz_id: int, user_id: int):
    with get_conn() as c:
        row = c.execute("""
            SELECT COUNT(*) as count
            FROM quiz_results
            WHERE quiz_id = ? AND user_id = ?;
        """,(quiz_id,user_id)).fetchone()
    return row["count"]