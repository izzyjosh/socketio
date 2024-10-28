import socketio
import asyncio

# Initialize the Socket.IO client
sio = socketio.AsyncClient()

@sio.event
async def connect():
    pass

@sio.event
async def response(data):
    print(f"Received from server: {data}")

@sio.event
async def disconnect():
    print("Disconnected from server")

async def main():
    try:
    # Connect to the serve
        await sio.connect("http://127.0.0.1:8000?username=joshua")
        await sio.emit("message", "Hello everyone")

        await sio.wait()
    
    except socketio.exceptions.ConnectionError as e:
        print(f"failed to connect {e}")

# Run the client
asyncio.run(main())
