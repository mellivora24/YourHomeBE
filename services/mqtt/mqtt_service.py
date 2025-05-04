from core.interfaces import IMQTTService
import paho.mqtt.client as mqtt
import json
import time
from typing import List


class MQTTService(IMQTTService):
    def __init__(self, broker: str, port: int):
        self.client = mqtt.Client()
        self.broker = broker
        self.port = port
        self.client.connect(broker, port)

    async def get_available_ports(self, home_id: int) -> List[int]:
        topic_request = f"yourhome/{home_id}/ports/request"
        topic_response = f"yourhome/{home_id}/ports/response"
        available_ports = []

        def on_message(client, userdata, msg):
            nonlocal available_ports
            available_ports = json.loads(msg.payload.decode())

        self.client.on_message = on_message
        self.client.subscribe(topic_response)
        self.client.publish(topic_request, "get_available_ports")

        self.client.loop_start()
        time.sleep(2)  # Đợi phản hồi
        self.client.loop_stop()
        return available_ports

    async def send_command(self, device_id: int, command: str):
        topic = f"yourhome/{device_id}"
        self.client.publish(topic, command)


mqtt_service = MQTTService("broker.hivemq.com", 1883)