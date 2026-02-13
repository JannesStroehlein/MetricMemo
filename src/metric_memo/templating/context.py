from datetime import datetime, timedelta, timezone

from src.metric_memo.templating.filters import (
    format_bytes,
    format_percent,
    format_timedelta,
    from_epoch,
    get_date_range,
)


def build_template_globals(
    time_selection: str,
    query_prom,
    query_prom_raw,
    query_loki,
    query_loki_top,
    query_loki_raw,
):
    start_date, end_date = get_date_range(time_selection)

    return {
        "time_selection": time_selection,
        "start_date": start_date,
        "end_date": end_date,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "now": datetime.now(timezone.utc),
        "query_prom": query_prom,
        "query_prom_raw": query_prom_raw,
        "query_loki": query_loki,
        "query_loki_top": query_loki_top,
        "query_loki_raw": query_loki_raw,
    }


def build_template_filters():
    return {
        "to_timedelta": lambda x: timedelta(seconds=int(x)),
        "from_epoch": from_epoch,
        "fmt_bytes": format_bytes,
        "fmt_pct": format_percent,
        "fmt_timedelta": format_timedelta,
    }
