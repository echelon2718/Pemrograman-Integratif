import asyncio
import websockets

async def communicate():
    async with websockets.connect("ws://localhost:8000") as websocket:
        welcome_message = await websocket.recv()
        print(f"Terima pesan dari server: {welcome_message}")

        while True:
            message = input("Masukkan pesan: ")
            await websocket.send(message)

            res = await websocket.recv()
            print(f"Bot: {res}")

asyncio.get_event_loop().run_until_complete(communicate())