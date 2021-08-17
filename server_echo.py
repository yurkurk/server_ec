# Importing the relevant libraries
import websockets
import asyncio

PORT = 7890

print("Server On Port " + str(PORT))


async def echo(websocket, path):
    try:
        async for message in websocket:
            await websocket.send(message)
    except websockets.exceptions.ConnectionClosed as e:
        print("A client just disconnected")

start_server = websockets.serve(echo, "localhost", PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

