from fastapi import WebSocket

class ConnectionManager:

    def __init__(self):

        self.active_connections = {}

    async def connect(
        self,
        email:str,
        websocket:WebSocket
    ):

        await websocket.accept()

        self.active_connections[email] = websocket

    def disconnect(self, email:str):

        if email in self.active_connections:

            del self.active_connections[email]

    async def send_personal_message(

        self,
        email:str,
        message:str
    ):

        websocket = self.active_connections.get(email)

        if websocket:

            await websocket.send_text(message)

manager = ConnectionManager()