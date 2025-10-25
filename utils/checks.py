from pyrogram.types import Message
from pyrogram import Client

async def is_user_admin(bot: Client, message: Message):
    try:
        user = message.from_user
        member = await bot.get_chat_member(message.chat.id, user.id)
        return member.status in ("administrator", "creator")
    except Exception:
        return False
