from app.database.init_db import get_conn

def insert_test_users():

    users = [
        ("bobice@example.com", "gigachad", "Heslo123", 0, 0),
        ("random@ez.cz", "uniuquenick", "Heslo123", 0, 0),
        ("ericcartman@example.com", "playerultimate67", "Heslo123", 0, 0),
        ("kylebrowlovski@example.com", "ihatecartman", "Heslo123", 0, 0),
        ("drakethegod@example.com", "godsplan89", "Heslo123", 0, 0),
        ("eminemiloveyou@example.com", "eminemlover41", "Heslo123", 0, 0)
    ]

    quizzes = [
        (1,"The Bite of 87 Quiz", "Test your memory and detective skills with this quiz about the legendary incident from the Five Nights at Freddy's series. Do you know the truth?", 2, "database/quiz_img/fnaf.jpg"),
        (2,"Web development", "Are you a beginner or an experienced developer? Verify how well you know HTML, CSS, JavaScript, and the core pillars of modern web development.", 1, "database/quiz_img/our-service-web.webp"),
        (3,"Ukraine war", "A quiz focused on the key events and facts concerning the war in Ukraine. Test your awareness of this ongoing current conflict.", 3, "database/quiz_img/War-in-Ukraine-UkraineWar_06_0.jpeg"),
        (4,"Best Filmakers", "Dive into the world of cinematography. Test your knowledge of iconic directors, their films, and their influence on the art of cinema.", 1, "database/quiz_img/who-are-the-best-directors-of-all-time.webp"),
    ]

    with get_conn() as c:
        for email, nickname, password, score, role_id in users:
            c.execute(
                """
                INSERT OR IGNORE INTO users (email, nickname, password_hash, score, role_id)
                VALUES (?, ?, ?, ?, ?)
                """,
                (email, nickname, password, score, role_id)
            )
        c.commit()

    with get_conn() as c:
        for id, title, description, user_id, image_path in quizzes:
            c.execute(
                """
                INSERT OR REPLACE INTO quizzes (id, title, description, user_id, image_path)
                VALUES (?, ?, ?, ?, ?)
                """,
                (id, title, description, user_id, image_path)
            )
        c.commit()

    #TESTOVACI OTAZKY A ODPOVEDI PRO UCEL TESTOVANI

    with get_conn() as c:
        c.executescript("""
                        -- Q1
            INSERT INTO questions (id, quiz_id, text) VALUES (1, 1, 'Která postava je nejčastěji spojována s Bite of 87?');
            INSERT INTO answers (question_id, text, is_correct) VALUES
                (1, 'Freddy Fazbear', 0),
                (1, 'Foxy', 0),
                (1, 'Mangle', 1),
                (1, 'Golden Freddy', 0);
            
            -- Q2
            INSERT INTO questions (id, quiz_id, text) VALUES (2, 1, 'V kterém roce se měl incident Bite of 87 odehrát?');
            INSERT INTO answers (question_id, text, is_correct) VALUES
                (2, '1983', 0),
                (2, '1987', 1),
                (2, '1993', 0),
                (2, '2015', 0);
            
            -- Q3
            INSERT INTO questions (id, quiz_id, text) VALUES (3, 1, 'Jaké zranění je podle teorií nejčastěji spojováno s Bite of 87?');
            INSERT INTO answers (question_id, text, is_correct) VALUES
                (3, 'Zlomená ruka', 0),
                (3, 'Amputace nohy', 0),
                (3, 'Poškození čelisti', 0),
                (3, 'Trauma frontálního laloku', 1);
            
            -- Q4
            INSERT INTO questions (id, quiz_id, text) VALUES (4, 1, 'Ve které hře se o Bite of 87 poprvé mluví?');
            INSERT INTO answers (question_id, text, is_correct) VALUES
                (4, 'Five Nights at Freddy''s 1', 1),
                (4, 'Five Nights at Freddy''s 2', 0),
                (4, 'Five Nights at Freddy''s 3', 0),
                (4, 'Sister Location', 0);
                            
                        -- Q1
            INSERT INTO questions (id, quiz_id, text) VALUES (5,2, 'Co znamená zkratka HTML?');
            INSERT INTO answers (question_id, text, is_correct) VALUES
                (5, 'HyperText Markup Language', 1),
                (5, 'Hyper Transfer Machine Language', 0),
                (5, 'High-Tech Modern Layout', 0),
                (5, 'Home Tool Markup Line', 0);
            
            -- Q2
            INSERT INTO questions (id, quiz_id, text) VALUES (6,2, 'Která vlastnost v CSS slouží k nastavení barvy textu?');
            INSERT INTO answers (question_id, text, is_correct) VALUES
                (6, 'font-style', 0),
                (6, 'text-color', 0),
                (6, 'color', 1),
                (6, 'font-color', 0);
            
            -- Q3
            INSERT INTO questions (id, quiz_id, text) VALUES (7,2, 'Který z následujících je datový typ v JavaScriptu?');
            INSERT INTO answers (question_id, text, is_correct) VALUES
                (7, 'integer', 0),
                (7, 'float', 0),
                (7, 'object', 1),
                (7, 'character', 0);
            
            -- Q4
            INSERT INTO questions (id, quiz_id, text) VALUES (8,2, 'Co dělá příkaz console.log() v JavaScriptu?');
            INSERT INTO answers (question_id, text, is_correct) VALUES
                (8, 'Vypíše text do HTML dokumentu', 0),
                (8, 'Otevře nové okno', 0),
                (8, 'Zapíše data do lokálního souboru', 0),
                (8, 'Vypíše informaci do vývojářské konzole', 1);

            -- Q1
            INSERT INTO questions (id, quiz_id, text) VALUES (9,3, 'V kterém roce začala plnohodnotná invaze Ruska na Ukrajinu?');
            INSERT INTO answers (question_id, text, is_correct) VALUES
                (9, '2014', 0),
                (9, '2020', 0),
                (9, '2022', 1),
                (9, '2023', 0);
            
            -- Q2
            INSERT INTO questions (id, quiz_id, text) VALUES (10,3, 'Které hlavní město bylo v prvních týdnech invaze jedním z hlavních cílů?');
            INSERT INTO answers (question_id, text, is_correct) VALUES
                (10, 'Lvov', 0),
                (10, 'Kyjev', 1),
                (10, 'Charkov', 0),
                (10, 'Dnipro', 0);
            
            -- Q3
            INSERT INTO questions (id, quiz_id, text) VALUES (11,3, 'Která země je hlavním agresorem v konfliktu?');
            INSERT INTO answers (question_id, text, is_correct) VALUES
                (11, 'Polsko', 0),
                (11, 'Rusko', 1),
                (11, 'Moldavsko', 0),
                (11, 'Bělorusko', 0);
            
            -- Q4
            INSERT INTO questions (id, quiz_id, text) VALUES (12,3, 'Které moře je strategicky důležité kvůli bojům na jihu Ukrajiny?');
            INSERT INTO answers (question_id, text, is_correct) VALUES
                (12, 'Baltské', 0),
                (12, 'Černé moře', 1),
                (12, 'Kaspické', 0),
                (12, 'Marmarské', 0);
            
            
            -- Q1
            INSERT INTO questions (id, quiz_id, text) VALUES (13,4, 'Kdo režíroval film Inception?');
            INSERT INTO answers (question_id, text, is_correct) VALUES
                (13, 'Quentin Tarantino', 0),
                (13, 'Christopher Nolan', 1),
                (13, 'Steven Spielberg', 0),
                (13, 'James Cameron', 0);
            
            -- Q2
            INSERT INTO questions (id, quiz_id, text) VALUES (14,4, 'Který režisér je známý svou symetrií a vizuálním stylem?');
            INSERT INTO answers (question_id, text, is_correct) VALUES
                (14, 'Martin Scorsese', 0),
                (14, 'Wes Anderson', 1),
                (14, 'Ridley Scott', 0),
                (14, 'Denis Villeneuve', 0);
            
            -- Q3
            INSERT INTO questions (id, quiz_id, text) VALUES (15,4, 'Kdo stojí za trilogií Pán prstenů?');
            INSERT INTO answers (question_id, text, is_correct) VALUES
                (15, 'Peter Jackson', 1),
                (15, 'George Lucas', 0),
                (15, 'Tim Burton', 0),
                (15, 'Ron Howard', 0);
            
            -- Q4
            INSERT INTO questions (id, quiz_id, text) VALUES (16,4, 'Který film natočil Quentin Tarantino?');
            INSERT INTO answers (question_id, text, is_correct) VALUES
                (16, 'Fight Club', 0),
                (16, 'Django Unchained', 1),
                (16, 'Gladiator', 0),
                (16, 'Shutter Island', 0);

        """)

    print("✅ Test users inserted successfully!")


if __name__ == "__main__":
    insert_test_users()
