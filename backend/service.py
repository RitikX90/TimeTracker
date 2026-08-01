# import 
from datetime import datetime
from database import (
    create_session,
    update_session,
    get_sessions,
    delete_sessionDB,
    get_one_session,
    get_all_active_session
)

def start_session(subject,  notes):
    start_time = datetime.now().isoformat()
    session_id=create_session(subject, start_time, notes)
    return dict(get_one_session(session_id))

def get_active_session():
    row = get_all_active_session()
    if row is None:
        return None
    return dict(row)

def stop_session(id):
    data = get_one_session(id)
    if data is None:
     return {"error": "No active session"}
    
    end_dt=datetime.now()
    # calculate duration 
    start_time = data["start_time"]
    start_dt = datetime.fromisoformat(start_time)
    duration = int((end_dt-start_dt).total_seconds())
    end_time = end_dt.isoformat()

    update_session(id, end_time, duration)
    return dict(data)

def get_all_sessions():
    rows = get_sessions()

    return ([dict(row) for row in rows])

def delete_session(id):
    data = delete_sessionDB(id)
    if data is None:
        return {"error": "Session not found"}
    
    return dict(data)
