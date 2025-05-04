from fastapi import APIRouter, Depends
from services.log.log_service import LogService
from routes.auth import get_current_user

router = APIRouter()

@router.get("/logs/{device_id}")
async def get_logs(device_id: int, start_time: str = None, end_time: str = None, user_id: str = Depends(get_current_user)):
    from datetime import datetime
    start = datetime.fromisoformat(start_time) if start_time else None
    end = datetime.fromisoformat(end_time) if end_time else None
    logs = await LogService.get_logs(device_id, start_time=start, end_time=end)
    return logs