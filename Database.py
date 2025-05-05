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
            
            # Create user statistics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_statistics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    topic TEXT NOT NULL,
                    total_questions INTEGER DEFAULT 0,
                    correct_questions INTEGER DEFAULT 0,
                    total_marks_earned INTEGER DEFAULT 0,
                    total_possible_marks INTEGER DEFAULT 0,
                    average_time_per_question REAL DEFAULT 0,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    UNIQUE(user_id, topic)
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

    def update_user_statistics(self, username, topic, is_correct, marks_earned, total_marks, time_taken):
        """Update user statistics for a specific topic"""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                # Get user_id
                cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
                user_id = cursor.fetchone()[0]
                
                # Update or insert statistics
                cursor.execute("""
                    INSERT INTO user_statistics (
                        user_id, topic, total_questions, correct_questions,
                        total_marks_earned, total_possible_marks, average_time_per_question
                    )
                    VALUES (?, ?, 1, ?, ?, ?, ?)
                    ON CONFLICT(user_id, topic) DO UPDATE SET
                        total_questions = total_questions + 1,
                        correct_questions = correct_questions + ?,
                        total_marks_earned = total_marks_earned + ?,
                        total_possible_marks = total_possible_marks + ?,
                        average_time_per_question = (
                            (average_time_per_question * (total_questions - 1) + ?) / total_questions
                        ),
                        last_updated = CURRENT_TIMESTAMP
                """, (
                    user_id, topic, 
                    1 if is_correct else 0, marks_earned, total_marks, time_taken,
                    1 if is_correct else 0, marks_earned, total_marks, time_taken
                ))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error updating user statistics: {e}")
            return False

    def get_user_statistics(self, username, topic=None):
        """Get statistics for a user, optionally filtered by topic"""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                # Get user_id
                cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
                user_id = cursor.fetchone()[0]
                
                if topic:
                    cursor.execute("""
                        SELECT topic, total_questions, correct_questions,
                               total_marks_earned, total_possible_marks,
                               average_time_per_question, last_updated
                        FROM user_statistics
                        WHERE user_id = ? AND topic = ?
                    """, (user_id, topic))
                else:
                    cursor.execute("""
                        SELECT topic, total_questions, correct_questions,
                               total_marks_earned, total_possible_marks,
                               average_time_per_question, last_updated
                        FROM user_statistics
                        WHERE user_id = ?
                        ORDER BY topic
                    """, (user_id,))
                
                results = cursor.fetchall()
                return [{
                    'topic': row[0],
                    'total_questions': row[1],
                    'correct_questions': row[2],
                    'total_marks_earned': row[3],
                    'total_possible_marks': row[4],
                    'average_time_per_question': row[5],
                    'last_updated': row[6],
                    'accuracy': (row[2] / row[1] * 100) if row[1] > 0 else 0,
                    'mark_percentage': (row[3] / row[4] * 100) if row[4] > 0 else 0
                } for row in results]
        except Exception as e:
            print(f"Error getting user statistics: {e}")
            return []

    def get_user_overall_statistics(self, username):
        """Get overall statistics for a user across all topics"""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                # Get user_id
                cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
                user_id = cursor.fetchone()[0]
                
                cursor.execute("""
                    SELECT 
                        SUM(total_questions) as total_questions,
                        SUM(correct_questions) as correct_questions,
                        SUM(total_marks_earned) as total_marks_earned,
                        SUM(total_possible_marks) as total_possible_marks,
                        AVG(average_time_per_question) as avg_time_per_question
                    FROM user_statistics
                    WHERE user_id = ?
                """, (user_id,))
                
                result = cursor.fetchone()
                if result and result[0] is not None:  # Check if there are any statistics
                    return {
                        'total_questions': result[0],
                        'correct_questions': result[1],
                        'total_marks_earned': result[2],
                        'total_possible_marks': result[3],
                        'average_time_per_question': result[4],
                        'overall_accuracy': (result[1] / result[0] * 100) if result[0] > 0 else 0,
                        'overall_mark_percentage': (result[2] / result[3] * 100) if result[3] > 0 else 0
                    }
                return {
                    'total_questions': 0,
                    'correct_questions': 0,
                    'total_marks_earned': 0,
                    'total_possible_marks': 0,
                    'average_time_per_question': 0,
                    'overall_accuracy': 0,
                    'overall_mark_percentage': 0
                }
        except Exception as e:
            print(f"Error getting overall statistics: {e}")
            return {
                'total_questions': 0,
                'correct_questions': 0,
                'total_marks_earned': 0,
                'total_possible_marks': 0,
                'average_time_per_question': 0,
                'overall_accuracy': 0,
                'overall_mark_percentage': 0
            }

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

    def update_password(self, username, new_password):
        """Update a user's password"""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                password_hash = self.hash_password(new_password)
                cursor.execute(
                    "UPDATE users SET password_hash = ? WHERE username = ?",
                    (password_hash, username)
                )
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating password: {e}")
            return False

    def update_username(self, old_username, new_username):
        """Update a user's username"""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                # Get user_id
                cursor.execute("SELECT id FROM users WHERE username = ?", (old_username,))
                user_id = cursor.fetchone()[0]
                
                # Update username
                cursor.execute(
                    "UPDATE users SET username = ? WHERE id = ?",
                    (new_username, user_id)
                )
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating username: {e}")
            return False

    def delete_user(self, username):
        """Delete a user and all their associated data"""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                # Get user_id
                cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
                user_id = cursor.fetchone()[0]
                
                # Delete user's statistics
                cursor.execute("DELETE FROM user_statistics WHERE user_id = ?", (user_id,))
                
                # Delete user's marks
                cursor.execute("DELETE FROM marks WHERE user_id = ?", (user_id,))
                
                # Delete user
                cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
                
                conn.commit()
                return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False


