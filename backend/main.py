from datetime import datetime, timezone

from fastapi import (
    FastAPI,
    WebSocket,
    WebSocketDisconnect,
    HTTPException
)

from fastapi.middleware.cors import (
    CORSMiddleware
)


from database import (
    create_user,
    get_user,
    save_message,
    get_messages
)


from auth import (
    hash_password,
    verify_password,
    create_token,
    verify_token
)


from manager import ConnectionManager


app = FastAPI(
    title="Real-Time Chat & Notification Service",
    version="1.0.0"
)


# -------------------------
# CORS
# -------------------------

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


manager = ConnectionManager()


# -------------------------
# HOME
# -------------------------

@app.get("/")
async def root():

    return {
        "message": "Real-Time Chat Service is running"
    }


# -------------------------
# REGISTER
# -------------------------

@app.post("/register")
async def register(
    username: str,
    password: str
):

    if len(username) < 3:

        raise HTTPException(
            status_code=400,
            detail="Username must be at least 3 characters"
        )


    if len(password) < 6:

        raise HTTPException(
            status_code=400,
            detail="Password must be at least 6 characters"
        )


    existing_user = await get_user(
        username
    )


    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )


    hashed_password = hash_password(
        password
    )


    await create_user(
        username,
        hashed_password
    )


    return {
        "message": "User registered successfully"
    }


# -------------------------
# LOGIN
# -------------------------

@app.post("/login")
async def login(
    username: str,
    password: str
):

    user = await get_user(
        username
    )


    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )


    password_valid = verify_password(
        password,
        user["password"]
    )


    if not password_valid:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )


    token = create_token(
        username
    )


    return {

        "access_token": token,

        "token_type": "bearer"
    }


# -------------------------
# CHAT HISTORY
# -------------------------

@app.get("/rooms/{room_id}/messages")
async def room_messages(
    room_id: str,
    token: str
):

    username = verify_token(
        token
    )


    if not username:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )


    messages = await get_messages(
        room_id
    )


    return messages


# -------------------------
# WEBSOCKET
# -------------------------

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    room_id: str,
    token: str
):

    username = verify_token(
        token
    )


    # Reject invalid token

    if not username:

        await websocket.close(
            code=1008
        )

        return


    # Connect user

    await manager.connect(
        websocket,
        room_id,
        username
    )


    # Notify room

    await manager.broadcast(
        room_id,
        {
            "type": "notification",

            "message":
                f"{username} joined the room"
        }
    )


    try:

        while True:

            # Receive message

            data = await websocket.receive_json()


            content = data.get(
                "content",
                ""
            ).strip()


            if not content:

                continue


            # Create message

            message = {

                "type": "message",

                "username": username,

                "room_id": room_id,

                "content": content,

                "timestamp":
                    datetime.now(
                        timezone.utc
                    ).isoformat()
            }


            # Save to MongoDB

            await save_message(
                message
            )


            # Send to everyone

            await manager.broadcast(
                room_id,
                message
            )


    except WebSocketDisconnect:

        manager.disconnect(
            room_id,
            username
        )


        # Notify room

        await manager.broadcast(
            room_id,
            {
                "type": "notification",

                "message":
                    f"{username} left the room"
            }
        )