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

##Vytvoreni kvizu

def save_image(image):
    """
    Uloží obrázek do složky a vrátí final path.
    """
    if not image:
        return "database/quiz_img/default.png"

    filename = f"{uuid.uuid4()}_{image.filename}"
    save_path = f"app/database/quiz_img/{filename}"

    with open(save_path, "wb") as f:
        f.write(image)

    return f"database/quiz_img/{filename}"

def create_quiz(payload: dict, image_bytes: bytes | None, user_id: int = 1):
    """
    Uloží kvíz + otázky + odpovědi.
    """
    title = payload["title"]
    desc = payload["description"]
    questions = payload["questions"]

    # Obrázek
    image_path = save_image(image_bytes)

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