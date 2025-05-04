from fastapi import FastAPI
from routes import auth, dashboard, device, history, admin, account
from services.websocket.websocket_service import websocket_service
from fastapi.websockets import WebSocket

app = FastAPI()

app.include_router(auth.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(device.router, prefix="/api")
app.include_router(history.router, prefix="/api")
app.include_router(admin.router, prefix="/api")
app.include_router(account.router, prefix="/api")

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket_service.connect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=5050, reload=True)