from datetime import datetime

def format_timestamp(timestamp: str) -> str:
    return datetime.fromisoformat(timestamp).strftime("%Y-%m-%d %H:%M:%S")