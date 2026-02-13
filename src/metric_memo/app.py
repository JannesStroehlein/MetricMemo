from datetime import datetime

from prometheus_api_client.prometheus_connect import PrometheusConnect
from requests.auth import HTTPBasicAuth

from .clients.loki_client import LokiClient
from .config.settings import Settings
from .delivery.email_sender import EmailSender
from .templating.context import build_template_filters, build_template_globals
from .templating.filters import get_date_range
from .templating.renderer import TemplateRenderer


class MetricMemoApp:
    def __init__(self, settings: Settings, time_selection: str = "7d"):
        self.settings = settings
        self.time_selection = time_selection

        self.prom = PrometheusConnect(
            url=settings.prom.url,
            disable_ssl=False,
            auth=(
                HTTPBasicAuth(settings.prom.user, settings.prom.password)
                if settings.prom.use_auth
                else None
            ),
        )

        self.loki = LokiClient(
            url=settings.loki.url,
            user=settings.loki.user if settings.loki.use_auth else None,
            password=settings.loki.password if settings.loki.use_auth else None,
        )

        self.email_sender = EmailSender(settings.smtp)

    def _template_renderer(self) -> TemplateRenderer:
        return TemplateRenderer(
            globals_=build_template_globals(
                self.time_selection,
                self.query_prom,
                self.query_prom_raw,
                self.query_loki,
                self.query_loki_top,
                self.query_loki_raw,
            ),
            filters=build_template_filters(),
        )

    def query_prom(self, query: str) -> int | str:
        try:
            res = self.prom.custom_query(query)
            return int(float(res[0]["value"][1])) if res else 0
        except Exception as e:
            return f"Error: {e}"

    def query_prom_raw(self, query: str) -> list:
        try:
            return self.prom.custom_query(query)
        except Exception as e:
            print(f"Prometheus Error: {e}")
            return []

    def query_loki(self, query: str) -> list[dict]:
        try:
            full_query = f"topk(5, sum by (message) (count_over_time({query} [{self.time_selection}])))"
            results = self.loki.query_raw(full_query)
            return [
                {
                    "count": int(float(item["value"][1])),
                    "message": item["metric"].get("message", "No message label found"),
                }
                for item in results
            ]
        except Exception as e:
            print("Error querying loki", e)
            return []

    def query_loki_top(self, selector: str, label: str, limit: int = 10) -> list[dict]:
        try:
            results = self.loki.query_top(selector, label, limit, self.time_selection)
            return sorted(results, key=lambda x: x["count"], reverse=True)
        except Exception as e:
            print(f"Loki Error on {label}: {e}")
            return []

    def query_loki_raw(self, logql: str, limit: int = 50) -> list[dict]:
        try:
            start_date, end_date = get_date_range(self.time_selection)
            results = self.loki.query_range(
                logql,
                start=start_date,
                end=end_date,
                limit=limit,
                direction="BACKWARD",
            )

            flattened = []
            for stream in results:
                labels = stream.get("stream", {})
                for ts_ns, line in stream.get("values", []):
                    flattened.append(
                        {
                            "timestamp": int(ts_ns),
                            "message": line,
                            "labels": labels,
                        }
                    )

            flattened.sort(key=lambda x: x["timestamp"], reverse=True)
            return flattened
        except Exception as e:
            print(f"Loki Raw Query Error: {e}")
            return []

    def render_html(self, path: str):
        return self._template_renderer().render_file(path)

    def render_email_subject(self, template_str: str):
        renderer = TemplateRenderer(
            globals_={
                "time_selection": self.time_selection,
                "date": datetime.now().strftime("%Y-%m-%d"),
            }
        )
        return renderer.render_string(template_str)

    def send_email(self, path: str, subject: str):
        html_body = self.render_html(path)
        self.email_sender.send_html(self.settings.recipients, subject, html_body)
