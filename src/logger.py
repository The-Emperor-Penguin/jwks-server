import os
import uuid
import sqlite3
from datetime import datetime, UTC
from dotenv import load_dotenv

class AuthLog:
    def __init__(self):
        load_dotenv()
        self.databasepath =  os.getenv("DATABASENAME")
        self.keypassword = os.getenv("KEYPASSWORD")
        with sqlite3.connect(self.databasepath) as conn:
            cursor = conn.cursor()
            cursor.execute(''' 
                CREATE TABLE IF NOT EXISTS auth_logs(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_ip TEXT NOT NULL,
                request_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_id INTEGER,  
                FOREIGN KEY(user_id) REFERENCES users(id)
                );
            ''')
        
    def logAuth(self, UID: int, IP: str):
        if not isinstance(UID, int) or not isinstance(IP, str):
            raise TypeError
        try:
            with sqlite3.connect(self.databasepath) as conn:
                cursor = conn.cursor()
                cursor.execute('''INSERT INTO auth_logs (request_ip, user_id) VALUES (?, ?)''', (IP, UID))

        except Exception as err:
            print(err)