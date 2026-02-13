""""
This module defines a simple HTTP server to render the email template for development/testing purposes.
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from metric_memo import MetricMemo

class TemplateDevServer:
    """
    A simple HTTP server to render the email template for development/testing purposes.
    This allows you to see how the email will look in a browser without actually sending it.
    """
    def __init__(self, app: "MetricMemo", template_path: str, port: int):
        self.app = app
        self.template_path = template_path
        self.port = port

    def start(self):
        """
        Start a simple HTTP server that renders the email template for development/testing purposes.
        """

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
