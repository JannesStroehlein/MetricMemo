"""
Utility functions for Jinja2 templates, such as date formatting and time range parsing.
"""
from datetime import timedelta, datetime, timezone
import re

TIME_SELECTION_REGEX = r"(?P<num>\d+)(?P<unit>\w)"

def get_start_date(end_date: datetime, number: int, unit: str):
    match unit:
        case "h":
            return end_date - timedelta(hours=number)
        case "d":
            return end_date - timedelta(days=number)
        case _:
            raise ValueError("Invalid time selection")


def get_date_range(selector: str):
    """
    Returns the start and end date for a LogQL/PromQL time selector like 7d or 24h
    """
    end_date = datetime.now()
    match = re.search(TIME_SELECTION_REGEX, selector)
    if not match:
        raise RuntimeError(f"Invalid time selection format: {selector}")

    number = match.group("num")
    unit = match.group("unit")

    return (get_start_date(end_date, int(number), unit), end_date)


def from_epoch(epoch_time):
    return datetime.fromtimestamp(epoch_time, timezone.utc)


def format_bytes(size):
    # Converts raw bytes to GB/TB
    power = 2**30
    n = size / power
    if n > 1024:
        return f"{n/1024:.2f} TB"
    return f"{n:.2f} GB"


def format_percent(val):
    return f"{val:.2f}%"


def format_timedelta(td: timedelta):
    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0:
        parts.append(f"{seconds}s")
    return " ".join(parts)
