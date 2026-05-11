from fastapi import WebSocket


class ConnectionManager:

    def __init__(self):

        self.active_connections = {}

    async def connect(
        self,
        user_email,
        websocket: WebSocket
    ):

        await websocket.accept()

        self.active_connections[user_email] = websocket

    def disconnect(self, user_email):

        self.active_connections.pop(
            user_email,
            None
        )

    async def send_message(
        self,
        user_email,
        message
    ):

        websocket = self.active_connections.get(
            user_email
        )

        if websocket:

            await websocket.send_text(message)


manager = ConnectionManager()