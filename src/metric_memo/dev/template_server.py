"""
This module implements a simple development server for previewing the rendered HTML templates.
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Callable


class TemplateDevServer:
    def __init__(self, render_html: Callable[[str], str], template_path: str, port: int):
        self.render_html = render_html
        self.template_path = template_path
        self.port = port

    def start(self):
        render_html = self.render_html
        template_path = self.template_path

        class RequestHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                html = render_html(template_path)
                self.wfile.write(html.encode("utf-8"))

        server_address = ("", self.port)
        httpd = HTTPServer(server_address, RequestHandler)
        print(f"Starting template dev server at http://localhost:{self.port}")
        httpd.serve_forever()
