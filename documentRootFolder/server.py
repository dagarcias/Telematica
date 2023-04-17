import http.server
import logging
import socketserver
import threading

PORT = 8000

class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            with open('index.html', 'rb') as f:
                html_content = f.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html_content)
        elif self.path == '/template1':
            with open('template1.html', 'rb') as f:
                html_content = f.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html_content)

        elif self.path == '/template2':
            with open('template2.html', 'rb') as f:
                html_content = f.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html_content)

        elif self.path == '/template3':
            with open('template3.html', 'rb') as f:
                html_content = f.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html_content)

        else:
            self.send_error(404, "Page/File Not Found")

        # Registro de evento
        logger.info(f"GET {self.path} {self.headers['User-Agent']}")

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        # Registro de evento
        logger.info(f"HEAD {self.path} {self.headers['User-Agent']}")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Hello POST: " + body)

        # Registro de evento
        logger.info(f"POST {self.path} {self.headers['User-Agent']} {content_length} {body}")

    def send_error(self, code, message=None, explain=None):
        self.send_response(code, message)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        if code == 404:
            self.wfile.write(b"Page/File Not Found")
        elif code == 400:
            self.wfile.write(b"Bad Request")
        else:
            self.wfile.write(b"Error")

        # Registro de evento
        logger.warning(f"Error {code} {self.path} {self.headers['User-Agent']}")

# Configuración del registro de eventos
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("servidor")

class ThreadedHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

Handler = MyHTTPRequestHandler

with ThreadedHTTPServer(("", PORT), Handler) as httpd:
    print("Servidor iniciado en el puerto", PORT)
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    try:
        server_thread.join()
    except KeyboardInterrupt:
        pass
    httpd.shutdown()
