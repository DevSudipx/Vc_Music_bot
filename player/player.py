import asyncio
from loguru import logger
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import InputStream
from pytgcalls.types.input_stream import AudioPiped
from pyrogram import Client
from collections import defaultdict, deque
from db.mongo import db
from .yt import get_audio_source

class Song:
    def __init__(self, title, source, duration, webpage_url):
        self.title = title
        self.source = source
        self.duration = duration
        self.webpage_url = webpage_url

class Player:
    def __init__(self, app: Client):
        self.app = app
        self.pytg = PyTgCalls(app)
        self.queues = defaultdict(deque)  # chat_id -> deque of (Song, requester)
        self.current = {}  # chat_id -> Song
        self.lock = asyncio.Lock()

    async def start(self):
        await self.pytg.start()
        logger.info("PyTgCalls started.")

    async def stop(self):
        await self.pytg.stop()
        logger.info("PyTgCalls stopped.")

    async def play(self, chat_id: int, query: str, requester_id: int):
        info = await get_audio_source(query)
        song = Song(info['title'], info['source'], info.get('duration'), info.get('webpage_url'))
        self.queues[chat_id].append((song, requester_id))
        if chat_id not in self.current:
            await self._start_next(chat_id)

    async def _start_next(self, chat_id: int):
        if not self.queues.get(chat_id):
            self.current.pop(chat_id, None)
            return
        song, requester = self.queues[chat_id].popleft()
        self.current[chat_id] = song
        logger.info(f"Starting playback: {song.title}")
        audio = AudioPiped(song.source)
        try:
            await self.pytg.join_group_call(
                chat_id,
                InputStream(audio),
            )
        except Exception as e:
            logger.error(f"Error joining group call for {chat_id}: {e}")

    async def skip(self, chat_id:int):
        try:
            await self.pytg.leave_group_call(chat_id)
        except Exception:
            pass
        await self._start_next(chat_id)

    async def pause(self, chat_id:int):
        try:
            await self.pytg.pause_stream(chat_id)
        except Exception as e:
            logger.error(f"Pause error: {e}")

    async def resume(self, chat_id:int):
        try:
            await self.pytg.resume_stream(chat_id)
        except Exception as e:
            logger.error(f"Resume error: {e}")

    async def stop(self, chat_id:int):
        try:
            await self.pytg.leave_group_call(chat_id)
        except Exception as e:
            logger.error(e)
        self.queues.pop(chat_id, None)
        self.current.pop(chat_id, None)
