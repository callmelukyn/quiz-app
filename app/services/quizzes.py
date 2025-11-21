from fastapi import UploadFile
from app.database.database import get_conn
import uuid

def get_all_quizzes():
    with get_conn() as c:
        rows = c.execute(
            """
            SELECT
                q.image_path,
                q.title,
                q.description,
                u.nickname,
                q.id,
                u.id as user_id
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
                q.id,
                u.id as user_id
            FROM quizzes q
            JOIN users u ON q.user_id = u.id
            WHERE q.id = ?;
            """,(id,)
        ).fetchall()
        return rows

def get_quiz_full(quiz_id: int):
    with get_conn() as c:
        quiz = c.execute("""
            SELECT id, title, description, image_path
            FROM quizzes
            WHERE id = ?;
        """, (quiz_id,)).fetchone()

        if not quiz:
            return None

        questions = c.execute("""
            SELECT id, text
            FROM questions
            WHERE quiz_id = ?
            ORDER BY id ASC;
        """, (quiz_id,)).fetchall()

        quiz_data = {
            "id": quiz["id"],
            "title": quiz["title"],
            "description": quiz["description"],
            "image_path": quiz["image_path"],
            "questions": []
        }

        for q in questions:
            q_id = q["id"]
            answers = c.execute("""
                SELECT id, text, is_correct
                FROM answers
                WHERE question_id = ?
                ORDER BY id ASC;
            """, (q_id,)).fetchall()

            quiz_data["questions"].append({
                "id": q_id,
                "text": q["text"],
                "answers": [
                    {"id": a["id"], "text": a["text"], "correct": a["is_correct"]}
                    for a in answers
                ]
            })

    return quiz_data

def delete_quiz(quiz_id: int, current_user_id : int):
    with get_conn() as c:
        owner = c.execute("""
            SELECT COUNT(*) as count
            FROM quizzes
            WHERE id = ?
                AND user_id = ?;
        """,(quiz_id,current_user_id)).fetchone()
        if owner["count"] == 0:
            return False
        else:
            c.execute("""
                DELETE FROM quizzes WHERE id = ?;
            """, (quiz_id,))
            c.commit()
            return True

def update_quiz(quiz_id: int, payload: dict, image: UploadFile | None):
    title = payload["title"]
    description = payload["description"]
    questions = payload["questions"]

    with get_conn() as c:
        #update obecne info
        if image:
            image_path = save_image(image)
            c.execute("""
                UPDATE quizzes
                SET title = ?, description = ?, image_path = ?
                WHERE id = ?;
            """, (title, description, image_path, quiz_id))
        else:
            c.execute("""
                UPDATE quizzes
                SET title = ?, description = ?
                WHERE id = ?;
            """, (title, description, quiz_id))

        #delete staré otázky + odpovědi
        c.execute("""
            DELETE FROM answers WHERE question_id IN (SELECT id FROM questions WHERE quiz_id = ?);
        """, (quiz_id,))
        c.execute("""
            DELETE FROM questions WHERE quiz_id = ?;
        """, (quiz_id,))

        #nové otázky + odpovědi
        for q in questions:
            qcur = c.execute("""
                INSERT INTO questions (quiz_id, text)
                VALUES (?, ?)
            """, (quiz_id, q["text"]))
            q_id = qcur.lastrowid

            for ans in q["answers"]:
                c.execute("""
                    INSERT INTO answers (question_id, text, is_correct)
                    VALUES (?, ?, ?)
                """, (q_id, ans["text"], ans["correct"]))

        c.commit()

def get_mine_quizzes(id: int):
    with get_conn() as c:
        rows = c.execute(
            """
            SELECT
                q.image_path,
                q.title,
                q.description,
                u.nickname,
                u.id as user_id,
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
            SELECT COALESCE(ROUND(AVG(score),2), 0) as average_score
            FROM quiz_results
            WHERE quiz_id = ?;
        """,(quiz_id,)).fetchone()
    return row["average_score"]

def get_your_average_score(quiz_id: int, user_id: int):
    with get_conn() as c:
        row = c.execute("""
            SELECT COALESCE(ROUND(AVG(score),2), 0) as average_score
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