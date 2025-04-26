import mysql.connector

def connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # default XAMPP password
        database="resume_tool"
    )

def insert_resume(name, email, skills, match_score):
    conn = connect()
    cursor = conn.cursor()
    query = "INSERT INTO resumes (name, email, skills, match_score) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, email, skills, match_score))
    conn.commit()
    conn.close()
