from app.database.init_db import get_conn

def insert_test_users():
    users = [
        ("bobice@example.com", "gigachad", "Heslo123", 235),
        ("laixcz@seznam.cz", "callmelukyn", "Heslo123", 6767),
        ("ericcartman@example.com", "playerultimate67", "Heslo123", 200),
        ("kylebrowlovski@example.com", "ihatecartman", "Heslo123", 682),
        ("drakethegod@example.com", "godsplan89", "Heslo123", 937),
        ("eminemiloveyou@example.com", "eminemlover41", "Heslo123", 2137)
    ]

    quizzes = [
        ("Integrals", "Test your knowledge of integrals! From basic rules to advanced integration techniques. Ideal for students of mathematics and engineering.", 1, "database/quiz_img/algebraic-integrals-hero.png"),
        ("The Bite of 87 Quiz", "Test your memory and detective skills with this quiz about the legendary incident from the Five Nights at Freddy's series. Do you know the truth?", 2, "database/quiz_img/fnaf.jpg"),
        ("WW2 Warriors", "A quiz for military history enthusiasts! Test your knowledge of famous generals, brave soldiers, and key figures of World War II.", 4, "database/quiz_img/ww2w.jpg"),
        ("Web development", "Are you a beginner or an experienced developer? Verify how well you know HTML, CSS, JavaScript, and the core pillars of modern web development.", 1, "database/quiz_img/our-service-web.webp"),
        ("Testing quiz", "This is just a testing card to see how everything looks. Also the image above is default.", 4, "database/quiz_img/default.png"),
        ("ENG B2 Conditionals", "A practice quiz focusing on English conditional sentences (Conditionals) at the B2 level. Master the zero, first, second, third, and mixed types!", 2, "database/quiz_img/zero-conditional.new_.png"),
        ("Ukraine war", "A quiz focused on the key events and facts concerning the war in Ukraine. Test your awareness of this ongoing current conflict.", 3, "database/quiz_img/War-in-Ukraine-UkraineWar_06_0.jpeg"),
        ("Ultimate E-Shop Quiz", "Are you an online shopping guru? This quiz will test your knowledge of e-shops, trends, logistics, and digital marketing. Get ready for the challenge!", 4, "database/quiz_img/1632412102.jpg"),
        ("Best Filmakers", "Dive into the world of cinematography. Test your knowledge of iconic directors, their films, and their influence on the art of cinema.", 1, "database/quiz_img/who-are-the-best-directors-of-all-time.webp"),
        ("Lotteries around the world", "Feeling lucky? A quiz about the most famous lotteries, their rules, history, and the highest jackpots globally. Give it a try!", 5, "database/quiz_img/f5aa8bacc5d9f761eb536ee764a7200c69b26d8314accae1b83f92236f187703.jpg")
    ]

    with get_conn() as c:
        for email, nickname, password, score in users:
            c.execute(
                """
                INSERT OR IGNORE INTO users (email, nickname, password_hash, score)
                VALUES (?, ?, ?, ?)
                """,
                (email, nickname, password, score),
            )
        c.commit()

    with get_conn() as c:
        for title, description, user_id, image_path in quizzes:
            c.execute(
                """
                INSERT OR IGNORE INTO quizzes (title, description, user_id, image_path)
                VALUES (?, ?, ?, ?)
                """,
                (title, description, user_id, image_path)
            )
        c.commit()

    print("✅ Test users inserted successfully!")


if __name__ == "__main__":
    insert_test_users()
