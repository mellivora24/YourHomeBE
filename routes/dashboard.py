from fastapi import APIRouter, Depends, HTTPException
from config.database import supabase
from routes.auth import get_current_user
from services.mqtt.mqtt_service import mqtt_service
from models.action import ActionCreate
from models.log import LogCreate
from config.event_bus import event_bus
from core.events import LogCreatedEvent

router = APIRouter()

@router.get("/dashboard/{home_id}")
async def get_dashboard(home_id: int, user_id: str = Depends(get_current_user)):
    devices = supabase.table("device").select("*").eq("home_id", home_id).execute().data
    sensors = supabase.table("sensor").select("*").execute().data
    return {"devices": devices, "sensors": sensors}

@router.post("/dashboard/control")
async def control_device(device_id: int, command: str, user_id: str = Depends(get_current_user)):
    device = supabase.table("device").select("home_id, status").eq("device_id", device_id).single().execute().data
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    await mqtt_service.send_command(device_id, command)

    if command in ["turn_on", "turn_off"]:
        new_status = True if command == "turn_on" else False
        supabase.table("device").update({"status": new_status}).eq("device_id", device_id).execute()

    action_data = ActionCreate(command=command, device_id=device_id)
    action_response = supabase.table("action").insert(action_data.dict()).execute()

    log_data = LogCreate(content=f"Device {device_id} executed command: {command}", device_id=device_id)
    log_response = supabase.table("log").insert(log_data.dict()).execute()
    log = log_response.data[0]
    await event_bus.publish(LogCreatedEvent(log["log_id"], log["device_id"], log["content"]))

    return {"message": "Command executed", "device_id": device_id, "command": command}

@router.post("/home")
async def create_home(name: str = "New Home", user_id: str = Depends(get_current_user)):
    # Lấy user_id từ auth_id
    user = supabase.table("users").select("user_id").eq("auth_id", user_id).single().execute().data
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_id_value = user["user_id"]

    # Thêm bản ghi mới vào bảng home
    home_data = {"user_id": user_id_value, "name": name}
    response = supabase.table("home").insert(home_data).execute()
    if not response.data:
        raise HTTPException(status_code=500, detail="Failed to create home")

    new_home_id = response.data[0]["home_id"]
    print(f"Created home with ID: {new_home_id}")

    return {"message": "Home created successfully", "home_id": new_home_id, "name": name}