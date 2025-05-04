from datetime import datetime
from config.database import supabase

class DeviceService:
    @staticmethod
    async def get_uptime(device_id: int) -> str:
        actions = supabase.table("action").select("*").eq("device_id", device_id).execute()
        last_on = None
        for action in actions.data:
            if action["command"] == "turn_on":
                last_on = datetime.fromisoformat(action["timestamp"])
                break
        if not last_on:
            return "0 seconds"
        uptime = datetime.utcnow() - last_on
        return str(uptime.total_seconds()) + " seconds"