#!/usr/bin/env python
"""Ultra-simple HTTP server for Railway testing."""

import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "healthy"}).encode())
        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Railway Test Server", "status": "ok"}).encode())
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    server = HTTPServer(('0.0.0.0', port), Handler)
    print(f"Server running on port {port}")
    server.serve_forever()