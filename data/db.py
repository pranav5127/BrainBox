import sqlite3
import os



def create_exam_table():
    project_folder = os.path.dirname(os.path.abspath(__file__))
    db_name = "question.db"
    db_path = os.path.join(project_folder, db_name)

    conn = sqlite3.connect(db_path)
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


def store_exam_values(file_path,evaluation_result):
    project_folder = os.path.dirname(os.path.abspath(__file__))
    db_name = "question.db"
    db_path = os.path.join(project_folder, db_name)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO exam_results (exam_file, evaluation, score) VALUES (?, ?, ?)",
        (file_path, evaluation_result.get("evaluation", ""), evaluation_result.get("score"))
    )
    conn.close()