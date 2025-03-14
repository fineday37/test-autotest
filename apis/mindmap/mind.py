from fastapi import APIRouter, WebSocket
from typing import List
from services.mindmap.mind import MindMapService
import typing

from starlette.websockets import WebSocketDisconnect

router = APIRouter()

connections: List[WebSocket] = []


@router.websocket("/ws/{mind_id}")
async def webSocket_endpoint(mind_id: int, webSocket: WebSocket):
    await MindMapService.mind(mind_id, webSocket)
