from motor.motor_asyncio import AsyncIOMotorClient


def get_client_mongodb_connection(
    uri: str,
    port: int,
    username: str,
    password: str,
) -> AsyncIOMotorClient:
    return AsyncIOMotorClient(f"mongodb://{username}:{password}@{uri}:{port}")
