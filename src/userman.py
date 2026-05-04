import os
import uuid
import sqlite3
from datetime import datetime, UTC
from dotenv import load_dotenv
from argon2 import PasswordHasher

class UserMan:
    def __init__(self):
        load_dotenv()
        self.databasepath =  os.getenv("DATABASENAME")
        self.keypassword = os.getenv("KEYPASSWORD")
        self.ph = PasswordHasher()
        #Create user table if it doesn't exist.
        with sqlite3.connect(self.databasepath) as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS users(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT NOT NULL UNIQUE,
                                password_hash TEXT NOT NULL,
                                email TEXT UNIQUE,
                                date_registered TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                last_login TIMESTAMP
                           )''')
    def create_user(self, username: str, email: str) -> str:
        password = str(uuid.uuid4())
        with sqlite3.connect(self.databasepath) as conn:
            cursor = conn.cursor()
            hashedpass = self.ph.hash(password)
            cursor.execute('''INSERT INTO users (username, password_hash, email, last_login) VALUES (?, ?, ?, ?)''',
                            (username, hashedpass, email, datetime.now(UTC)))
            return password
    def get_UID(self, username='', email='') -> int:
        """
        given a username it will return the UID of the user.
        WARNING currently email is not implemented but may be added later
        """
        if username == '':
            raise ValueError
        elif email != '':
            raise NotImplementedError
        else:
            try:
                with sqlite3.connect(self.databasepath) as conn:
                    row = conn.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
                    return row[0]
            except (sqlite3.OperationalError, sqlite3.ProgrammingError, TypeError, IndexError) as err:
                print(err)
                raise err