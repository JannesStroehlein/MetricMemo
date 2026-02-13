"""
This module contains the ReportRenderer class, 
which is responsible for rendering Jinja2 templates
"""
from datetime import datetime

from metric_memo.queries.service import QueryService
from metric_memo.templating.context import build_template_filters, build_template_globals
from metric_memo.templating.renderer import TemplateRenderer


class ReportRenderer:
    """
    Abstraction of the Jinja2 template rendering logic, 
    that is used across the application to render both HTML reports and email subjects.
    """
    def __init__(self, query_service: QueryService):
        self.query_service = query_service

    def _template_renderer(self) -> TemplateRenderer:
        return TemplateRenderer(
            globals_=build_template_globals(
                self.query_service.time_selection,
                self.query_service.query_prom,
                self.query_service.query_prom_raw,
                self.query_service.query_loki,
                self.query_service.query_loki_top,
                self.query_service.query_loki_raw,
            ),
            filters=build_template_filters(),
        )

    def render_html(self, path: str) -> str:
        return self._template_renderer().render_file(path)

    def render_email_subject(self, template_str: str) -> str:
        renderer = TemplateRenderer(
            globals_={
                "time_selection": self.query_service.time_selection,
                "date": datetime.now().strftime("%Y-%m-%d"),
            }
        )
        return renderer.render_string(template_str)
