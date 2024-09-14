from fastapi import APIRouter, WebSocket
from typing import List

from starlette.websockets import WebSocketDisconnect

router = APIRouter()

connections: List[WebSocket] = []


@router.websocket("/ws")
async def webSocket_endpoint(webSocket: WebSocket):
    # 允许 WebSocket 连接
    await webSocket.accept()
    connections.append(webSocket)
    try:
        while True:
            # 接收来自客户端的消息
            data = await webSocket.receive_text()
            print(f"Received message: {data}")

            # 处理消息并广播给所有连接的客户端
            for connection in connections:
                if connection is not webSocket:
                    await connection.send_text(data)
    except WebSocketDisconnect:
        # 从连接列表中移除断开的连接
        connections.remove(webSocket)
        print("Client disconnected")
