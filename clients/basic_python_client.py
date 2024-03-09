import asyncio
import websockets
import sys


async def receive_messages(user, uri):
    async with websockets.connect(uri, extra_headers={'user':user}) as websocket:
        while True:
            message = await websocket.recv()
            print(f"Received message: {message}")

async def main(user, uri):
    await receive_messages(user, uri)

if __name__ == "__main__":

    try:
        user = sys.argv[1]
        uri = sys.argv[2]
        asyncio.run(main(user, uri))

    except IndexError:
        print('You must to run the client launcher')
