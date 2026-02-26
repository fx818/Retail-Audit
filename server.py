#!/usr/bin/env python3
"""
Retail Auditor Dashboard Server
Run: python server.py  then open http://localhost:8080/index.html
"""
import http.server
import socketserver
import os
import json
from datetime import datetime

PORT = 8080

# Set working directory to script location
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class AuditorHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Enhanced CORS headers for better compatibility
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def do_OPTIONS(self):
        """Handle preflight OPTIONS requests"""
        self.send_response(200)
        self.end_headers()

    def log_message(self, format, *args):
        """Enhanced logging with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"  [{timestamp}] {args[0]} {args[1]}")

        # Log file uploads and API calls
        if len(args) > 2:
            path = args[1]
            if 'index.html' in path:
                print(f"    📄 Dashboard loaded")
            elif path.startswith('/webhook') or 'auditor' in path:
                print(f"    🔗 API call detected: {path}")

    def guess_type(self, path):
        """Enhanced MIME type detection"""
        mime_type = super().guess_type(path)

        # Ensure proper MIME types for our files
        if path.endswith('.html'):
            return 'text/html'
        elif path.endswith('.js'):
            return 'application/javascript'
        elif path.endswith('.css'):
            return 'text/css'
        elif path.endswith('.json'):
            return 'application/json'
        elif path.endswith(('.xlsx', '.xls')):
            return 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

        return mime_type

def main():
    """Main server function with error handling"""
    try:
        with socketserver.TCPServer(("", PORT), AuditorHandler) as server:
            server.allow_reuse_address = True

            print("🚀 Retail Auditor Dashboard Server")
            print("=" * 50)
            print(f"✅ Server running on http://localhost:{PORT}")
            print(f"📄 Dashboard: http://localhost:{PORT}/index.html")
            print(f"📁 Serving from: {os.getcwd()}")
            print("=" * 50)
            print("📊 Features enabled:")
            print("  • Excel file support (.xlsx, .xls)")
            print("  • CSV/TSV file support")
            print("  • CORS headers for n8n webhook")
            print("  • Enhanced error handling")
            print("=" * 50)
            print("💡 Press Ctrl+C to stop the server")
            print()

            server.serve_forever()

    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Port {PORT} is already in use!")
            print("   Try stopping other servers or use a different port")
        else:
            print(f"❌ Server error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
