import sqlite3
import os

class DatabaseService:
    def __init__(self, db_name="question.db"):
        self.project_folder = ".../data/"
        self.db_path = os.path.join(self.project_folder, db_name)

    def create_exam_table(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exam_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                exam_file TEXT NOT NULL,
                evaluation TEXT NOT NULL,
                score INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.close()

    def store_exam_values(self, file_path, evaluation_result):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO exam_results (exam_file, evaluation, score) VALUES (?, ?, ?)",
            (file_path, evaluation_result.get("evaluation", ""), evaluation_result.get("score"))
        )
        conn.close()

data=DatabaseService()
data.create_exam_table()