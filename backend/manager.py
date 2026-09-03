from collections import defaultdict


class ConnectionManager:

    def __init__(self):

        self.rooms = defaultdict(dict)


    async def connect(
        self,
        websocket,
        room_id,
        username
    ):

        await websocket.accept()

        self.rooms[room_id][username] = websocket


    def disconnect(
        self,
        room_id,
        username
    ):

        if room_id not in self.rooms:
            return

        self.rooms[room_id].pop(
            username,
            None
        )

        if not self.rooms[room_id]:

            del self.rooms[room_id]


    async def broadcast(
        self,
        room_id,
        message
    ):

        if room_id not in self.rooms:
            return


        disconnected_users = []


        for username, websocket in list(
            self.rooms[room_id].items()
        ):

            try:

                await websocket.send_json(
                    message
                )

            except Exception:

                disconnected_users.append(
                    username
                )


        for username in disconnected_users:

            self.disconnect(
                room_id,
                username
            )