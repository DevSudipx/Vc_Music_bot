import asyncio
from loguru import logger
from pyrogram import Client
from config import API_ID, API_HASH, STRING_SESSION, LOG_LEVEL
from player.player import Player
from handlers.commands import register_handlers
from db.mongo import init_db

logger.remove()
logger.add("logs/bot.log", level=LOG_LEVEL)
logger.add(lambda msg: print(msg, end=""), level=LOG_LEVEL)

app = Client(
    session_name=STRING_SESSION or "vc_music_userbot",
    api_id=API_ID,
    api_hash=API_HASH,
)

player = None

async def main():
    global player
    logger.info("Initializing DB...")
    await init_db()
    logger.info("Starting Pyrogram client...")
    await app.start()
    logger.success("Pyrogram started.")
    player = Player(app)
    await player.start()
    register_handlers(app, player)
    logger.success("Handlers registered. Bot ready.")
    from pyrogram import idle
    await idle()
    logger.info("Stopping...")
    await player.stop()
    await app.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Exited by user")
