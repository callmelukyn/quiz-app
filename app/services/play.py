from app.database.database import get_conn

def get_quiz_full(quiz_id: int):
    with get_conn() as c:

        quiz = c.execute("""
            SELECT id, title, description, image_path
            FROM quizzes
            WHERE id = ?;
        """, (quiz_id,)).fetchone()

        questions = c.execute("""
            SELECT id, text
            FROM questions
            WHERE quiz_id = ?;
        """, (quiz_id,)).fetchall()

        result = {
            "id": quiz[0],
            "title": quiz[1],
            "description": quiz[2],
            "image_path": quiz[3],
            "questions": []
        }

        for q in questions:
            answers = c.execute("""
                SELECT id, text, is_correct
                FROM answers
                WHERE question_id = ?;
            """, (q[0],)).fetchall()

            result["questions"].append({
                "id": q[0],
                "text": q[1],
                "answers": [
                    {"id": a[0], "text": a[1], "is_correct": a[2]}
                    for a in answers
                ]
            })

        return result

def log_quiz_attempt(quiz_id: int, user_id: int, score: int):
    with get_conn() as c:
        c.execute("""
            INSERT INTO quiz_results (quiz_id, user_id, score) VALUES (?, ?, ?);
        """,(quiz_id, user_id, score))
        c.commit()

def is_user_eligible_to_get_points(quiz_id: int, user_id: int):
    with get_conn() as c:
        row = c.execute("""
            SELECT COUNT(score) as count
            FROM quiz_results
            WHERE quiz_id = ? AND user_id = ? AND score = 100;
        """, (quiz_id, user_id)).fetchone()
        if row["count"] == 1:
            author = c.execute("""
                SELECT COUNT(*) as count
                FROM quizzes
                WHERE user_id = ?
                AND id = ?;
            """, (user_id, quiz_id)).fetchone()
            if author["count"] == 1:
                return False #pokud je majitel kvizu False
            else:
                return True #neni majitel kvizu
        else:
            return False #uzivatel má v logs vícekrát 100 Score, neni mozne dostat body znovu