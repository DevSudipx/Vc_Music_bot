from pyrogram import filters
from pyrogram.types import Message
from loguru import logger
from utils.checks import is_user_admin
from utils.lyrics import fetch_lyrics

def register_handlers(app, player):
    @app.on_message(filters.command("start") & filters.private)
    async def start(_, m: Message):
        await m.reply_text("Sup! I'm a VC Music Bot. Use /help in groups.")

    @app.on_message(filters.command("help"))
    async def help_cmd(_, m: Message):
        txt = (
            "/play <query|url> - play or queue\n"
            "/pause - pause playback\n"
            "/resume - resume\n"
            "/skip - skip current\n"
            "/stop - stop & clear queue\n"
            "/queue - see queue\n"
            "/lyrics <song name> - fetch lyrics\n"
        )
        await m.reply_text(txt)

    @app.on_message(filters.command("play") & filters.group)
    async def play_cmd(_, m: Message):
        chat_id = m.chat.id
        user = m.from_user
        if len(m.command) < 2:
            return await m.reply_text("Send /play <song name or url>")
        query = " ".join(m.command[1:])
        await m.reply_text(f"Searching `{query}` ...")
        try:
            await player.play(chat_id, query, user.id)
            await m.reply_text(f"Queued: `{query}`")
        except Exception as e:
            logger.error(e)
            await m.reply_text("Error while adding to queue.")

    @app.on_message(filters.command("skip") & filters.group)
    async def skip_cmd(_, m: Message):
        chat_id = m.chat.id
        if not await is_user_admin(_, m):
            return await m.reply_text("You need to be admin to skip.")
        await player.skip(chat_id)
        await m.reply_text("Skipped.")

    @app.on_message(filters.command("pause") & filters.group)
    async def pause_cmd(_, m: Message):
        chat_id = m.chat.id
        if not await is_user_admin(_, m):
            return await m.reply_text("Admin only.")
        await player.pause(chat_id)
        await m.reply_text("Paused.")

    @app.on_message(filters.command("resume") & filters.group)
    async def resume_cmd(_, m: Message):
        chat_id = m.chat.id
        if not await is_user_admin(_, m):
            return await m.reply_text("Admin only.")
        await player.resume(chat_id)
        await m.reply_text("Resumed.")

    @app.on_message(filters.command("stop") & filters.group)
    async def stop_cmd(_, m: Message):
        chat_id = m.chat.id
        if not await is_user_admin(_, m):
            return await m.reply_text("Admin only.")
        await player.stop(chat_id)
        await m.reply_text("Stopped and cleared queue.")

    @app.on_message(filters.command("queue") & filters.group)
    async def queue_cmd(_, m: Message):
        chat_id = m.chat.id
        q = player.queues.get(chat_id, [])
        if not q:
            return await m.reply_text("Queue is empty.")
        text = "Now Playing:\n"
        current = player.current.get(chat_id)
        if current:
            text += f"• {current.title}\n\nUpcoming:\n"
        for idx, (song, uid) in enumerate(q, start=1):
            text += f"{idx}. {song.title}\n"
        await m.reply_text(text)

    @app.on_message(filters.command("lyrics") & filters.group)
    async def lyrics_cmd(_, m: Message):
        if len(m.command) < 2:
            return await m.reply_text("Usage: /lyrics <song name>")
        query = " ".join(m.command[1:])
        res = await fetch_lyrics(query)
        await m.reply_text(res or "Lyrics not found.")
