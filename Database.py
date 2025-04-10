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
            
            # Create marks table to store exam results
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS marks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    paper TEXT NOT NULL,
                    question_id TEXT NOT NULL,
                    marks_earned INTEGER NOT NULL,
                    total_marks INTEGER NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    UNIQUE(user_id, paper, question_id)
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

    def add_marks(self, username, paper, question_id, marks_earned, total_marks):
        """Add or update marks for a user's question"""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                # Get user_id
                cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
                user_id = cursor.fetchone()[0]
                
                # Insert or update marks
                cursor.execute("""
                    INSERT INTO marks (user_id, paper, question_id, marks_earned, total_marks)
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(user_id, paper, question_id) 
                    DO UPDATE SET marks_earned = excluded.marks_earned
                """, (user_id, paper, question_id, marks_earned, total_marks))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error adding marks: {e}")
            return False

    def get_user_marks(self, username, paper=None):
        """Get all marks for a user, optionally filtered by paper"""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                # Get user_id
                cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
                user_id = cursor.fetchone()[0]
                
                if paper:
                    cursor.execute("""
                        SELECT paper, question_id, marks_earned, total_marks, timestamp
                        FROM marks
                        WHERE user_id = ? AND paper = ?
                        ORDER BY timestamp DESC
                    """, (user_id, paper))
                else:
                    cursor.execute("""
                        SELECT paper, question_id, marks_earned, total_marks, timestamp
                        FROM marks
                        WHERE user_id = ?
                        ORDER BY timestamp DESC
                    """, (user_id,))
                
                return cursor.fetchall()
        except Exception as e:
            print(f"Error getting marks: {e}")
            return []

    def get_paper_summary(self, username, paper):
        """Get summary statistics for a specific paper"""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                # Get user_id
                cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
                user_id = cursor.fetchone()[0]
                
                cursor.execute("""
                    SELECT 
                        SUM(marks_earned) as total_earned,
                        SUM(total_marks) as total_possible,
                        COUNT(*) as question_count
                    FROM marks
                    WHERE user_id = ? AND paper = ?
                """, (user_id, paper))
                
                result = cursor.fetchone()
                if result:
                    return {
                        'total_earned': result[0] or 0,
                        'total_possible': result[1] or 0,
                        'question_count': result[2] or 0
                    }
                return {'total_earned': 0, 'total_possible': 0, 'question_count': 0}
        except Exception as e:
            print(f"Error getting paper summary: {e}")
            return {'total_earned': 0, 'total_possible': 0, 'question_count': 0}

    def get_all_users_marks(self, paper=None):
        """Get marks for all users, optionally filtered by paper"""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                
                if paper:
                    cursor.execute("""
                        SELECT u.username, m.paper, m.question_id, m.marks_earned, m.total_marks, m.timestamp
                        FROM marks m
                        JOIN users u ON m.user_id = u.id
                        WHERE m.paper = ?
                        ORDER BY m.timestamp DESC
                    """, (paper,))
                else:
                    cursor.execute("""
                        SELECT u.username, m.paper, m.question_id, m.marks_earned, m.total_marks, m.timestamp
                        FROM marks m
                        JOIN users u ON m.user_id = u.id
                        ORDER BY m.timestamp DESC
                    """)
                
                return cursor.fetchall()
        except Exception as e:
            print(f"Error getting all users' marks: {e}")
            return []

    def get_all_users_summary(self):
        """Get summary statistics for all users"""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT 
                        u.username,
                        m.paper,
                        SUM(m.marks_earned) as total_earned,
                        SUM(m.total_marks) as total_possible,
                        COUNT(*) as question_count
                    FROM marks m
                    JOIN users u ON m.user_id = u.id
                    GROUP BY u.username, m.paper
                    ORDER BY u.username, m.paper
                """)
                
                return cursor.fetchall()
        except Exception as e:
            print(f"Error getting all users summary: {e}")
            return []


