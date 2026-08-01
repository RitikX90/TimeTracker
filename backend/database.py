import sqlite3
from datetime import datetime

DATABASE = "study_tracker.db"
def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory= sqlite3.Row
    return conn

def initialize_database():
    conn= get_connection()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS study_sessions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT NOT NULL,
        start_time TEXT NOT NULL,
        end_time TEXT,
        duration INTEGER,
        notes TEXT
    )""")
    conn.commit()
    conn.close()

def get_sessions():
    conn= get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM study_sessions WHERE end_time IS NOT NULL")
    rows = cursor.fetchall()
    conn.close()
    return rows

def create_session(subject, start_time, notes):
    conn = get_connection()
    cursor= conn.cursor()
    
    cursor.execute("""
            INSERT INTO study_sessions(subject, start_time, notes) 
            VALUES(?,?,?)
            """,(subject, start_time, notes))
    
    conn.commit()
    session_id=cursor.lastrowid
    conn.close()
    # becuase session id will need when we end the session
    return session_id


def update_session(id, end_time, duration):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("""UPDATE study_sessions
                    SET end_time=?,
                    duration =?
                    WHERE id =? """,(end_time, duration, id))
    
    conn.commit()
    cursor.execute("SELECT * FROM study_sessions WHERE id=?",(id,))
    data = cursor.fetchone()
    conn.close()
    return data


def get_one_session(id):
    conn = get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM study_sessions WHERE id=?",(id,))
    data = cursor.fetchone()
    conn.close()
    return data

def get_all_active_session():
    conn = get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM study_sessions WHERE end_time IS NULL")
    data = cursor.fetchone()
    conn.close()
    return data

def delete_sessionDB(session_id):
    data = get_one_session(session_id)
    if data is None:
        # no id fonud 
        return None
    
    conn = get_connection()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM study_sessions WHERE id=?",(session_id,))
    if cursor.rowcount==0:
        conn.close()
        return None
    
    conn.commit()
    conn.close()
    # this is used by frontend as confirmation 
    return data
    