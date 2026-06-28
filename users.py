"""
users.py

SQLite User Management
"""

import sqlite3

from pathlib import Path

from backend.security import hash_password


class UserDatabase:

    def __init__(self):

        self.db_path = "database/mine_safety.db"

        Path(self.db_path).parent.mkdir(

            parents=True,

            exist_ok=True

        )

        self.conn = sqlite3.connect(

            self.db_path,

            check_same_thread=False

        )

        self.conn.row_factory = sqlite3.Row

        self.cursor = self.conn.cursor()

        self.create_table()

        self.create_default_admin()

    # ======================================================

    def create_table(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS users(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE,

            full_name TEXT,

            password TEXT,

            role TEXT,

            active INTEGER DEFAULT 1,

            last_login TEXT

        )

        """)

        self.conn.commit()

    # ======================================================

    def create_default_admin(self):

        self.cursor.execute(

            """

            SELECT *

            FROM users

            WHERE username='admin'

            """

        )

        row = self.cursor.fetchone()

        if row:

            return

        self.cursor.execute(

            """

            INSERT INTO users(

                username,

                full_name,

                password,

                role,

                active

            )

            VALUES(?,?,?,?,?)

            """,

            (

                "admin",

                "Administrator",

                hash_password("admin123"),

                "admin",

                1

            )

        )

        self.cursor.execute(

            """

            INSERT INTO users(

                username,

                full_name,

                password,

                role,

                active

            )

            VALUES(?,?,?,?,?)

            """,

            (

                "operator",

                "Mine Operator",

                hash_password("operator123"),

                "operator",

                1

            )

        )

        self.conn.commit()

    # ======================================================

    def get_user(

        self,

        username

    ):

        self.cursor.execute(

            """

            SELECT *

            FROM users

            WHERE username=?

            """,

            (username,)

        )

        row = self.cursor.fetchone()

        if row:

            return dict(row)

        return None

    # ======================================================

    def list_users(self):

        self.cursor.execute(

            """

            SELECT

                id,

                username,

                full_name,

                role,

                active,

                last_login

            FROM users

            ORDER BY id

            """

        )

        return [

            dict(row)

            for row in self.cursor.fetchall()

        ]

    # ======================================================

    def add_user(

        self,

        username,

        full_name,

        password,

        role

    ):

        self.cursor.execute(

            """

            INSERT INTO users(

                username,

                full_name,

                password,

                role

            )

            VALUES(?,?,?,?)

            """,

            (

                username,

                full_name,

                hash_password(password),

                role

            )

        )

        self.conn.commit()

    # ======================================================

    def update_password(

        self,

        username,

        password

    ):

        self.cursor.execute(

            """

            UPDATE users

            SET password=?

            WHERE username=?

            """,

            (

                hash_password(password),

                username

            )

        )

        self.conn.commit()

    # ======================================================

    def delete_user(

        self,

        username

    ):

        if username == "admin":

            return False

        self.cursor.execute(

            """

            DELETE FROM users

            WHERE username=?

            """,

            (username,)

        )

        self.conn.commit()

        return True

    # ======================================================

    def set_last_login(

        self,

        username,

        timestamp

    ):

        self.cursor.execute(

            """

            UPDATE users

            SET last_login=?

            WHERE username=?

            """,

            (

                timestamp,

                username

            )

        )

        self.conn.commit()


db = UserDatabase()


def get_user(username):

    return db.get_user(username)


def list_users():

    return db.list_users()


def add_user(

    username,

    full_name,

    password,

    role

):

    db.add_user(

        username,

        full_name,

        password,

        role

    )


def update_password(

    username,

    password

):

    db.update_password(

        username,

        password

    )


def delete_user(username):

    return db.delete_user(username)


def set_last_login(

    username,

    timestamp

):

    db.set_last_login(

        username,

        timestamp

    )