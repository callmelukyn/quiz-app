from database import get_conn

def init_db():
    with get_conn() as c:
        # Role (user, admin)
        c.execute("""
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );
        """)

        # Naplnění výchozích rolí
        c.execute("""INSERT INTO roles(id, name) VALUES (0, 'user'),(1, 'moderator'), (2, 'admin');""")

        # Uživatelé
        c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            nickname TEXT NOT NULL,
            password_hash BLOB NOT NULL,
            role_id INTEGER REFERENCES roles(id) NOT NULL DEFAULT 0,
            is_active INTEGER NOT NULL DEFAULT 1,
            score INTEGER DEFAULT 0
        );
        """)

        # Kvízy
        c.execute("""
        CREATE TABLE IF NOT EXISTS quizzes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            image_path TEXT DEFAULT 'database/quiz_img/default.png',
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
         )""")

         #Otázky
        c.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quiz_id INTEGER REFERENCES quizzes(id) ON DELETE CASCADE,
                text TEXT NOT NULL
            );
            """)

        # Odpovědi
        c.execute("""
            CREATE TABLE IF NOT EXISTS answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id INTEGER REFERENCES questions(id) ON DELETE CASCADE,
                text TEXT NOT NULL,
                is_correct INTEGER NOT NULL DEFAULT 0
            );
            """)

        # Výsledky hraní kvízu
        c.execute("""
        CREATE TABLE IF NOT EXISTS quiz_results (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
               quiz_id INTEGER REFERENCES quizzes(id) ON DELETE CASCADE,
               score INTEGER DEFAULT 0,
               completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
           );
           """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
               session_id INTEGER PRIMARY KEY AUTOINCREMENT,
               user_id INTEGER NOT NULL,
               session_code TEXT NOT NULL UNIQUE
           );
           """)

        c.commit()


if __name__ == "__main__":
    init_db()
    print("✅ Database initialized successfully.")
