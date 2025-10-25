# Telegram VC Music Bot (Pyrogram + PyTgCalls)

Developer: @sudipx

Features:
- Play/pause/resume/skip/stop in group voice chats.
- Queue management, playlists, now-playing info.
- yt-dlp streaming from YouTube; direct file support.
- MongoDB (Motor) for persistent queues, playlists, stats.
- String session generator for fast setup.
- Deployment config for Replit / Render / Railway.

## Requirements
- Python 3.10+
- ffmpeg installed on host
- Telegram API_ID and API_HASH (from my.telegram.org)
- A Telegram Bot token (optional; main control is via user account string session)
- MongoDB URI (Atlas recommended)

## Environment Variables
Create a `.env` with:
```
API_ID=123456
API_HASH=your_api_hash
BOT_TOKEN=123456:ABC-DEF...
MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/dbname
STRING_SESSION=     # you will fill via session_generator.py
LOG_LEVEL=INFO
```

## Quick setup
1. `pip install -r requirements.txt`
2. Run `python session_generator.py` and follow prompts to produce `STRING_SESSION`.
3. Put `STRING_SESSION` and other env values in `.env` or set on host.
4. `python main.py`

## Deployment
- Replit: push the repo, add env vars in Replit UI, run.
- Render/Railway: configure env vars; use `Procfile`/`runtime.txt`.

## Notes
- ffmpeg must be available to stream; test with `ffmpeg -version`.
- This repo is modular. Add Spotify features or better lyrics API as needed.
