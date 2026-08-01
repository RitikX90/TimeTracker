import http.server
import socketserver
import json
from database import initialize_database
from service import (
    get_all_sessions,
    start_session,
    stop_session,
    get_active_session,
    delete_session,
    )



class StudyTrackerHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/sessions":
            data = get_all_sessions()
            self.send_json_response(data)

        elif self.path=="/api/active-session":
            row = get_active_session()
            if row is None:
                self.send_json_response(None, 200)
            else:
                self.send_json_response(row, 200)
        else:
            super().do_GET()

    def do_POST(self):
        if self.path=="/api/start":

            content_length = int(self.headers['content-length'])
            post_data_bytes = self.rfile.read(content_length)
            post_data_string = post_data_bytes.decode('utf-8')
            data = json.loads(post_data_string)
            session_data = start_session(data['subject'], data['notes'])
            response_data = {
                "message":"Session Started",
                "data": session_data
            }
            self.send_json_response(response_data, 201)

        elif self.path.startswith("/api/stop/"):
            try:
                session_id_string = self.path.split("/")[-1]
                session_id = int(session_id_string)
                session_data = stop_session(session_id)
                response_data = {
                    "message":"Session Stopped",
                    "session_data": session_data
                }
                self.send_json_response(response_data, 200)

            except ValueError:
                # If the frontend accidentally sends "/api/start/apple", 
                # int() will crash. This catches that error safely!
                self.send_error(400, "Invalid ID format. ID must be a number.")
        
    def do_DELETE(self):
        if self.path.startswith("/api/delete/"):
            session_id_string = self.path.split("/")[-1]
            session_id = int(session_id_string)
            session_data = delete_session(session_id)
            response_data = {
                "message":"Session Deleted",
                "session_data": session_data
            }
            self.send_json_response(response_data,200)
    def do_OPTIONS(self):
        self.send_response(204) # 204 No Content
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        
    def send_json_response(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type","application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))


def main():
    initialize_database()
    PORT = 8000
    with socketserver.TCPServer(("",PORT),StudyTrackerHandler) as httpd:
        print(f"Server is running on http://localhost:{PORT}")
        httpd.serve_forever()


if __name__ == "__main__":
    main()