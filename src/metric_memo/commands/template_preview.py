from src.metric_memo.app import MetricMemoApp
from src.metric_memo.dev.template_server import TemplateDevServer


def run_template_preview(app: MetricMemoApp, template_path: str, port: int):
    server = TemplateDevServer(app, template_path, port)
    server.start()
