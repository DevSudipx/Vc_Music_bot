import motor.motor_asyncio
from config import MONGO_URI
from loguru import logger

db = None

async def init_db():
    global db
    if not MONGO_URI:
        logger.warning("No MONGO_URI provided, using in-memory fallback.")
        db = None
        return
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
    db = client.get_default_database()
    # ensure indexes
    try:
        await db.playlists.create_index("owner")
        await db.queues.create_index("chat_id")
        await db.stats.create_index("user_id")
    except Exception:
        pass
    logger.info("MongoDB initialized")
