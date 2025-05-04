from config.database import supabase
from config.event_bus import event_bus
from core.events import DeviceAddedEvent
from services.mqtt.mqtt_service import mqtt_service
from datetime import datetime

class DeviceManager:
    async def create_device(self, device_data: dict) -> dict:
        # available_ports = await mqtt_service.get_available_ports(device_data["home_id"])
        # if device_data["port"] not in available_ports:
        #     raise ValueError("Port not available")
        device_data["created_at"] = datetime.utcnow().isoformat()
        response = supabase.table("device").insert(device_data).execute()
        device = response.data[0]
        await mqtt_service.send_command(device["device_id"], f"enable_port:{device['port']}")
        await event_bus.publish(DeviceAddedEvent(device["device_id"], device["home_id"]))
        return device

    async def update_device(self, device_id: int, device_data: dict) -> dict:
        response = supabase.table("device").update(device_data).eq("device_id", device_id).execute()
        return response.data[0]

    async def delete_device(self, device_id: int) -> dict:
        device = supabase.table("device").select("port", "home_id").eq("device_id", device_id).execute().data[0]
        response = supabase.table("device").delete().eq("device_id", device_id).execute()
        await mqtt_service.send_command(device_id, f"disable_port:{device['port']}")
        return response.data