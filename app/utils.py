from flask import current_app
from datetime import datetime
import pytz

def format_datetime(dt):
    """
    Format a datetime object or string to the application's locale and timezone.
    Args:
        dt (datetime | str): The datetime object or ISO string to format.
    Returns:
        str: The formatted datetime string.
    """
    if not dt:
        return "N/A"

    # Convert string to datetime if necessary
    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt)
        except ValueError:
            return "Invalid Date"

    # Get the configured timezone
    tz = current_app.config.get("TIMEZONE", pytz.UTC)

    # Convert and format the datetime
    localized_dt = dt.astimezone(tz)
    return localized_dt.strftime("%Y-%m-%d %H:%M:%S")
