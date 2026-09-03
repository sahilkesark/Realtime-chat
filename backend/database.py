from motor.motor_asyncio import AsyncIOMotorClient


MONGO_URL = "mongodb://localhost:27017"

client = AsyncIOMotorClient(MONGO_URL)

database = client["realtime_chat"]

users_collection = database["users"]

messages_collection = database["messages"]


async def create_user(username, password):

    existing_user = await users_collection.find_one(
        {"username": username}
    )

    if existing_user:
        return False

    await users_collection.insert_one({
        "username": username,
        "password": password
    })

    return True


async def get_user(username):

    return await users_collection.find_one(
        {"username": username}
    )


async def save_message(message):

    await messages_collection.insert_one(
        message
    )


async def get_messages(room_id):

    cursor = (
        messages_collection
        .find(
            {"room_id": room_id},
            {"_id": 0}
        )
        .sort("timestamp", 1)
        .limit(50)
    )

    return await cursor.to_list(
        length=50
    )