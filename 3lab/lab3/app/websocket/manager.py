import asyncio
from fastapi import WebSocket
from typing import Dict, List

connections: Dict[int, List[WebSocket]] = {}

async def connect(user_id: int, websocket: WebSocket):
    await websocket.accept()
    if user_id not in connections:
        connections[user_id] = []
    connections[user_id].append(websocket)

def disconnect(user_id: int, websocket: WebSocket):
    if user_id in connections:
        if websocket in connections[user_id]:
            connections[user_id].remove(websocket)
        if not connections[user_id]:  
            del connections[user_id]

def notify_progress(user_id: int, message: dict):
    if user_id in connections:
        for ws in connections[user_id]:
            try:
                loop = asyncio.get_event_loop()
                loop.create_task(ws.send_json(message))
            except Exception as e:
                print(f"[WebSocket Notify Error] {e}")
