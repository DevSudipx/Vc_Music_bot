import asyncio
from yt_dlp import YoutubeDL
from loguru import logger

YTDL_OPTS = {
    "format": "bestaudio/best",
    "quiet": True,
    "no_warnings": True,
    "cachedir": False,
}

async def get_audio_source(query: str):
    """
    If query is a URL, fetch direct audio URL. If not, search YouTube.
    Returns dict: {title, webpage_url, duration, source}
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _sync_extract, query)

def _sync_extract(query):
    with YoutubeDL(YTDL_OPTS) as ydl:
        try:
            if query.startswith("http"):
                info = ydl.extract_info(query, download=False)
            else:
                info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
            if 'formats' in info:
                for f in info['formats']:
                    if f.get('acodec') != 'none' and f.get('url'):
                        source = f['url']
                        break
                else:
                    source = info['formats'][0]['url']
            else:
                source = info.get('url')
            return {
                "title": info.get("title"),
                "webpage_url": info.get("webpage_url"),
                "duration": info.get("duration"),
                "source": source
            }
        except Exception as e:
            logger.error(f"yt-dlp error: {e}")
            raise
