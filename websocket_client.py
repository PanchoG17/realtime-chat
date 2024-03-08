import asyncio
import websockets
import json

uri = "ws://localhost:8000/chat/politic"
user = input("Enter your name:")


## Connect to consumer
async def connect_to_server():
    return await websockets.connect(uri, extra_headers={'user':user})


## Send message to consumer
async def send_message(websocket):

    try:
        while True:
            message = await get_input()
            data = {
                'message':message,
                'user':user
            }
            if data['message'].lower() == "quit":
                break

            await websocket.send(json.dumps(data))

    except websockets.ConnectionClosedError:
        print("Connection closed.")


## Receive incoming messages from consumer
async def receive_messages(websocket):
    try:
        while True:
            message = await websocket.recv()
            print("Received message:", message)

    except websockets.ConnectionClosedError:
        print("Connection closed.")


async def get_input():
    return await asyncio.to_thread(input, "Enter message (or type 'quit' to exit): ")


async def main():
    websocket = await connect_to_server()
    await asyncio.gather(send_message(websocket), receive_messages(websocket))


asyncio.run(main())