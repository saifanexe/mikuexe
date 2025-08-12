import threading
import asyncio
from flask import Flask
from telethon import TelegramClient
from telethon.sessions import StringSession
import config
import os
import signal
import sys
import bot_handlers
import user_handlers
from session import userbot, active_users, client_users, set_ping
from firebase import fetch_and_append_sessions
from config import bot

app = Flask(__name__)

@app.route('/')
def home():
    return "Flask app is running!"

# Use a lock to synchronize access to active_users set (since multiple threads)
active_users_lock = threading.Lock()

async def run_userbot(session_str):
    with active_users_lock:
        if session_str in active_users:
            print(f"Session already running: {session_str[:5]}...")
            return
        active_users.add(session_str)
    client = None
    try:
        client = TelegramClient(StringSession(session_str), config.API_ID, config.API_HASH)
        await client.start()
        user_handlers.register(client)  # Make sure this does not add duplicate handlers
        me = await client.get_me()
        client_users(me)
        print(f"Userbot started: {me.first_name}")
        # Remove session from userbot["client"] once started (optional)
        if session_str in userbot.get("client", []):
            userbot["client"].remove(session_str)
        await client.run_until_disconnected()
    except Exception as e:
        print(f"Error in userbot with session {session_str[:5]}...: {e}")
        # Clean up bad sessions from your storage if needed
        if session_str in userbot.get("client", []):
            userbot["client"].remove(session_str)
    finally:
        with active_users_lock:
            if session_str in active_users:
                active_users.remove(session_str)
        if client:
            await client.disconnect()
        print(f"Userbot stopped: {session_str[:5]}...")

async def manage_userbots():
    while True:
        sessions = userbot.get("client", [])
        with active_users_lock:
            running_sessions = active_users.copy()
        for session_str in sessions:
            if session_str not in running_sessions:
                print(f"Starting userbot for session: {session_str[:5]}...")
                asyncio.create_task(run_userbot(session_str))
        await asyncio.sleep(5)

async def run_main_bot():
    bot_client = TelegramClient('bot_session', config.API_ID, config.API_HASH)
    await bot_client.start(bot_token=config.BOT_TOKEN)
    set_ping()
    bot_handlers.register(bot_client)  # Make sure no duplicate registration
    me = await bot_client.get_me()
    bot["name"] = me.first_name
    bot["username"] = me.username
    bot["user_id"] = me.id
    print(f"{me.first_name} bot started")
    try:
        await bot_client.run_until_disconnected()
    finally:
        await bot_client.disconnect()
        print("Main bot stopped")

def start_userbot_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(manage_userbots())

def start_bot_thread():
    asyncio.run(run_main_bot())

def run_flask():
    port = int(os.getenv('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

def handle_exit(signum, frame):
    print("Received exit signal, shutting down...")
    sys.exit(0)

if __name__ == "__main__":
    # Register exit signals for graceful shutdown
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    fetch_and_append_sessions()
    bot_thread = threading.Thread(target=start_bot_thread, daemon=True)
    userbot_thread = threading.Thread(target=start_userbot_thread, daemon=True)
    bot_thread.start()
    userbot_thread.start()

    # Run flask in main thread (blocking)
    run_flask()