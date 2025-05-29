from fastapi import APIRouter, WebSocket, Depends
from app.services.auth import get_current_user
from app.websocket.manager import connect, disconnect

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, user=Depends(get_current_user)):
    await connect(user.id, websocket)
    try:
        while True:
            await websocket.receive_text()  
    except:
        disconnect(user.id)
