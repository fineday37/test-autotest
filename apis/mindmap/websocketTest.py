import asyncio
import websockets


async def test_websocket():
    uri = "ws://localhost:8103/api/mind/ws"  # WebSocket 服务器的 URI
    async with websockets.connect(uri) as websocket:
        # 发送消息
        message = "测试连接成功"
        await websocket.send(message)
        print(f"Sent message: {message}")

        # 接收响应
        response = await websocket.recv()
        print(f"Received response: {response}")


# 运行测试
asyncio.get_event_loop().run_until_complete(test_websocket())
