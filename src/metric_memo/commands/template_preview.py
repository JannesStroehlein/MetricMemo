"""
Subcommand to preview a template in a development server
"""
from metric_memo.app import RuntimeDependencies
from metric_memo.dev.template_server import TemplateDevServer


def run_template_preview(runtime: RuntimeDependencies, template_path: str, port: int):
    """
    Starts a development server that renders the specified template for previewing.
    """
    server = TemplateDevServer(runtime.report_renderer.render_html, template_path, port)
    server.start()
