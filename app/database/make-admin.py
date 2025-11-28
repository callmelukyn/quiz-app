from app.database.init_db import get_conn
def make_admin():
    admin = 2
    with get_conn() as c:
        c.execute(
            """
            UPDATE users 
            SET role_id = ?
            WHERE nickname = 'TestAdminProfile';
            """,(admin,)
        )
        c.commit()
        print("commited")

if __name__ == "__main__":
    make_admin()
