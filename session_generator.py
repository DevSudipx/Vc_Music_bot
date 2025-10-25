# run this once locally to create STRING_SESSION
from pyrogram import Client
from pyrogram import __version__ as pyv

api_id = int(input("API_ID: ").strip())
api_hash = input("API_HASH: ").strip()

with Client(":memory:", api_id=api_id, api_hash=api_hash) as app:
    print("Pyrogram v", pyv)
    print("Sign in in the opened console window if asked.")
    session = app.export_session_string()
    print("\n\n--- COPY THIS STRING SESSION ---\n")
    print(session)
    print("\n--- End ---\n")
