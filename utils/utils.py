from datetime import datetime
from datetime import timezone


def get_current_time():
    """Utils function for getting current time"""
    return datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
