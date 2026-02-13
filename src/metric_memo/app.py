"""
This module is responsible for building the runtime dependencies of the application.
"""
from dataclasses import dataclass

from prometheus_api_client.prometheus_connect import PrometheusConnect
from requests.auth import HTTPBasicAuth

from metric_memo.clients.loki_client import LokiClient
from metric_memo.config.settings import Settings
from metric_memo.delivery.email_sender import EmailSender
from metric_memo.queries.service import QueryService
from metric_memo.templating.report_renderer import ReportRenderer


@dataclass
class RuntimeDependencies:
    """
    Holds all the runtime dependencies for the application, 
    that are built once and passed around to different commands.
    """
    settings: Settings
    query_service: QueryService
    report_renderer: ReportRenderer
    email_sender: EmailSender


def build_runtime(settings: Settings, time_selection: str) -> RuntimeDependencies:
    prom = PrometheusConnect(
        url=settings.prom.url,
        disable_ssl=False,
        auth=(
            HTTPBasicAuth(settings.prom.user, settings.prom.password)
            if settings.prom.use_auth
            else None
        ),
    )

    loki = LokiClient(
        url=settings.loki.url,
        user=settings.loki.user if settings.loki.use_auth else None,
        password=settings.loki.password if settings.loki.use_auth else None,
    )

    query_service = QueryService(prom=prom, loki=loki, time_selection=time_selection)
    report_renderer = ReportRenderer(query_service)
    email_sender = EmailSender(settings.smtp)

    return RuntimeDependencies(
        settings=settings,
        query_service=query_service,
        report_renderer=report_renderer,
        email_sender=email_sender,
    )
