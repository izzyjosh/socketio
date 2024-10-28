import uvicorn
import socketio
from urllib.parse import parse_qs


sio = socketio.AsyncServer(async_mode="asgi")
app = socketio.ASGIApp(sio)

users = {}

async def broadcast(sid, data):
    print(f"message from {sid}: {data}")
    for key in users.keys():
        await sio.emit("response", f"{users[sid]}: {data}", to=key)

@sio.event
async def connect(sid, environ):

    query_params = parse_qs(environ.get("QUERY_STRING", ""))
    username = query_params.get("username", ["Anonymous"])[0]

    users.update({sid: username})
    #await sio.emit("response", f"{users[sid]} joined this chat", to=sid)
    await broadcast(sid, f"successfully joined this chat")

@sio.event
async def message(sid, data):
    print(f"message from {users[sid]}: {data}")

    await broadcast(sid, data)

@sio.event
async def disconnect(sid):
    print('disconnect ', users[sid])

if __name__ == '__main__':
    uvicorn.run(app)
