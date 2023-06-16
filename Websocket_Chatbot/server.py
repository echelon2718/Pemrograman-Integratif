import asyncio
import websockets
import openai

openai.api_key = "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"

def chatRes(text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=text,
        temperature=0.9,
        max_tokens=2000,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=["Human:", "Jacob:"]
    )
    return response.choices[0].text

async def handle_connection(websocket, path):
    text = "\Jacob:Halo, saya Jacob!\nHuman:"
    await websocket.send("Selamat datang!")

    try:
        while True:
            message = await websocket.recv()
            print(f"Terima pesan dari klien: {message}")

            text += f"{message}\Jacob:"
            response = chatRes(text)
            text += f"{response}\nHuman:"

            await websocket.send(response)
            print(f"Kirim balasan ke klien: {response}")
    except websockets.exceptions.ConnectionClosedOK:
        print("Koneksi ditutup oleh klien.")

start_server = websockets.serve(handle_connection, "localhost", 8000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()