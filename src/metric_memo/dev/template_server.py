from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.metric_memo.app import MetricMemoApp


class TemplateDevServer:
    def __init__(self, app: "MetricMemoApp", template_path: str, port: int):
        self.app = app
        self.template_path = template_path
        self.port = port

    def start(self):
        app = self.app
        template_path = self.template_path

        class RequestHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                html = app.render_html(template_path)
                self.wfile.write(html.encode("utf-8"))

        server_address = ("", self.port)
        httpd = HTTPServer(server_address, RequestHandler)
        print(f"Starting template dev server at http://localhost:{self.port}")
        httpd.serve_forever()
