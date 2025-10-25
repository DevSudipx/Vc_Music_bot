import aiohttp
from loguru import logger

async def fetch_lyrics(query: str):
    # Placeholder: uses lyrics.ovh style or other API
    async with aiohttp.ClientSession() as sess:
        try:
            return f"Lyrics lookup for `{query}` not implemented. Plug in Genius API."
        except Exception as e:
            logger.error(e)
            return None
