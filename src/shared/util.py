from datetime import datetime, timezone
import time


def get_timestamp():
    """
    Get the current Unix timestamp as an integer
    """

    return int(time.time())


def get_datetime():
    """
    Get the current date and time in the ISO 8601 UTC format
    """

    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
