import json

from fastapi import WebSocket
from typing import List
from starlette.websockets import WebSocketDisconnect
from models.mind_models import MindMapModel
from schemas.mindmap.mind import MindMapQuery

connections: List[WebSocket] = []


class MindMapService:
    @staticmethod
    async def mind(mind_id: int, webSocket: WebSocket):
        await webSocket.accept()
        connections.append(webSocket)
        try:
            while True:
                # 接收来自客户端的消息
                data = await webSocket.receive_text()
                if json.loads(data)["type"] == "open":
                    mind_data = await MindMapModel.get_list(mind_id, MindMapQuery.model_validate_json(data))
                    print(f"读取数据: {mind_data}")
                    for connection in connections:
                        # if connection is not webSocket:
                        await connection.send_json(mind_data[0])
                else:
                    mind_data = await MindMapModel.create_or_update(json.loads(data))
                    print(f"写入的数据: {mind_data}")
                    for connection in connections:
                        # if connection is not webSocket:
                        await connection.send_json(mind_data)

        except WebSocketDisconnect:
            # 从连接列表中移除断开的连接
            connections.remove(webSocket)
            print("Client disconnected")
