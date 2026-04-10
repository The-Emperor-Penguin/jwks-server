import sqlite3
import uuid
import os
from dotenv import load_dotenv
from argon2 import PasswordHasher
from datetime import datetime, UTC

class userman:
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
    def log_login(self, username: str) -> bool:
        return False