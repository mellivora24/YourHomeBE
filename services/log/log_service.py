from datetime import datetime
from config.database import supabase

class LogService:
    @staticmethod
    async def get_logs(device_id: int, start_time: datetime = None, end_time: datetime = None) -> list:
        query = supabase.table("log").select("*").eq("device_id", device_id)
        if start_time:
            query = query.gte("timestamp", start_time.isoformat())
        if end_time:
            query = query.lte("timestamp", end_time.isoformat())
        return query.execute().data