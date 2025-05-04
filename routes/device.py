from fastapi import APIRouter, Depends, HTTPException
from config.database import supabase
from routes.auth import get_current_user
from models.device import DeviceCreate
from models.sensor import SensorCreate
from postgrest.exceptions import APIError

router = APIRouter()

# Hàm đảm bảo room tồn tại, nếu không sẽ tạo mới
async def ensure_room_exists(room_id: int, home_id: int, user_id: str):
    try:
        # Lấy user_id thực tế từ auth_id
        user = supabase.table("users").select("user_id").eq("auth_id", user_id).single().execute().data
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user_id_value = user["user_id"]
    except APIError as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving user: {e.message}")

    try:
        # Kiểm tra home có thuộc về user không
        home = supabase.table("home").select("home_id").eq("home_id", home_id).eq("user_id", user_id_value).single().execute().data
        if not home:
            raise HTTPException(status_code=403, detail="Home does not belong to this user")
    except APIError as e:
        raise HTTPException(status_code=500, detail=f"Error verifying home: {e.message}")

    try:
        # Kiểm tra room đã tồn tại chưa
        supabase.table("room").select("room_id").eq("room_id", room_id).single().execute()
    except APIError as e:
        if e.code == "PGRST116":  # No rows returned
            # Tạo room mới nếu chưa tồn tại
            room_data = {
                "room_id": room_id,
                "home_id": home_id,
                "name": f"Room {room_id}"  # Tên mặc định
            }
            response = supabase.table("room").insert(room_data).execute()
            if not response.data:
                raise HTTPException(status_code=500, detail="Failed to create room")
            print(f"Created room with ID: {room_id}")
        else:
            raise HTTPException(status_code=500, detail=f"Error checking room: {e.message}")


# -------------------------------
# ROUTE: Tạo thiết bị mới
# -------------------------------
@router.post("/device")
async def create_device(device: DeviceCreate, user_id: str = Depends(get_current_user)):
    # Đảm bảo room tồn tại trước khi tạo device
    await ensure_room_exists(device.room_id, device.home_id, user_id)

    # Thêm thiết bị vào bảng device
    device_data = device.dict()
    response = supabase.table("device").insert(device_data).execute()
    if not response.data:
        raise HTTPException(status_code=500, detail="Failed to create device")

    new_device_id = response.data[0]["device_id"]
    print(f"Created device with ID: {new_device_id}")

    return {"message": "Device created successfully", "device_id": new_device_id}


# -------------------------------
# ROUTE: Cập nhật thiết bị
# -------------------------------
@router.put("/device/{device_id}")
async def update_device(device_id: int, device: DeviceCreate, user_id: str = Depends(get_current_user)):
    # Kiểm tra thiết bị có tồn tại không
    try:
        existing_device = supabase.table("device").select("home_id").eq("device_id", device_id).single().execute().data
        if not existing_device:
            raise HTTPException(status_code=404, detail="Device not found")
    except APIError as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving device: {e.message}")

    # Đảm bảo room tồn tại trước khi cập nhật
    await ensure_room_exists(device.room_id, device.home_id, user_id)

    # Cập nhật thiết bị
    device_data = device.dict()
    response = supabase.table("device").update(device_data).eq("device_id", device_id).execute()
    if not response.data:
        raise HTTPException(status_code=500, detail="Failed to update device")

    return {"message": "Device updated successfully", "device_id": device_id}


# -------------------------------
# ROUTE: Tạo cảm biến mới
# -------------------------------
@router.post("/sensor")
async def create_sensor(sensor: SensorCreate, user_id: str = Depends(get_current_user)):
    # Kiểm tra device có tồn tại không
    try:
        device = supabase.table("device").select("device_id, home_id").eq("device_id", sensor.device_id).single().execute().data
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")
        home_id = device["home_id"]
    except APIError as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving device: {e.message}")

    # Kiểm tra room tồn tại hay chưa, nếu chưa thì tạo
    try:
        supabase.table("room").select("room_id").eq("room_id", sensor.room_id).eq("home_id", home_id).single().execute()
    except APIError as e:
        if e.code == "PGRST116":  # No rows returned
            await ensure_room_exists(sensor.room_id, home_id, user_id)
        else:
            raise HTTPException(status_code=500, detail=f"Error checking room: {e.message}")

    # Thêm sensor vào bảng sensor
    sensor_data = sensor.dict()
    response = supabase.table("sensor").insert(sensor_data).execute()
    if not response.data:
        raise HTTPException(status_code=500, detail="Failed to create sensor")

    new_sensor_id = response.data[0]["sensor_id"]
    print(f"Created sensor with ID: {new_sensor_id}")

    return {"message": "Sensor created successfully", "sensor_id": new_sensor_id}
