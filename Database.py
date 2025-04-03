import sqlite3
import hashlib
import os

class Database:
    def __init__(self, db_file="Assets/Database/users.db"):
        self.db_file = db_file
        self.init_database()

    def init_database(self):
        """Initialize the database and create tables if they don't exist"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            # Create users table with autoincrementing ID, username (unique), and hashed password
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def hash_password(self, password):
        """Hash a password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def add_user(self, username, password):
        """Add a new user to the database"""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                password_hash = self.hash_password(password)
                cursor.execute(
                    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    (username, password_hash)
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            # Username already exists
            return False
        except Exception as e:
            print(f"Error adding user: {e}")
            return False

    def verify_user(self, username, password):
        """Verify user credentials"""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                password_hash = self.hash_password(password)
                cursor.execute(
                    "SELECT id FROM users WHERE username = ? AND password_hash = ?",
                    (username, password_hash)
                )
                result = cursor.fetchone()
                return result is not None
        except Exception as e:
            print(f"Error verifying user: {e}")
            return False

    def username_exists(self, username):
        """Check if a username already exists"""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
                result = cursor.fetchone()
                return result is not None
        except Exception as e:
            print(f"Error checking username: {e}")
            return False


