from fastapi import WebSocket
from config.database import supabase

class WebSocketService:
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        while True:
            data = await websocket.receive_text()
            await self.broadcast(data, websocket)

    async def broadcast(self, data: str, websocket: WebSocket):
        await websocket.send_text(f"Broadcast: {data}")

websocket_service = WebSocketService()