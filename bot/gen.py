from telethon import TelegramClient, events, errors
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError
from config import API_ID, API_HASH
import asyncio

async def gen_handle(client, event):
    chat_id = event.chat_id if hasattr(event, 'chat_id') else event.chat.id
    
    privacy = "🕵️‍♂️️ We value user privacy, so phone numbers and request history are not stored anywhere."
    await event.reply(f"📱 Send your phone number with country code (e.g. +91...)\n<blockquote>{privacy}</blockquote>", parse_mode="html")
    phone = await listen(client, chat_id)
    if not phone:
        return

    sent = await event.respond("Procceeding...")
    new_client = TelegramClient(StringSession(), API_ID, API_HASH)
    await new_client.connect()

    try:
        sent_code = await new_client.send_code_request(phone)
    except Exception:
        await sent.edit("Invalid phone number.")
        await new_client.disconnect()
        return

    await sent.edit("📩 Send the OTP you received (e.g., 1 2 3 4 5)")
    get_code = await listen(client, chat_id)  
    code = get_code.replace(" ", "")  

    try:
        await new_client.sign_in(phone=phone, code=code, phone_code_hash=sent_code.phone_code_hash)
    except SessionPasswordNeededError:
        await event.respond("🔒 Your account has 2FA enabled. Send your password:")
        password = await listen(client, chat_id)
        try:
            await new_client.sign_in(password=password)
        except Exception as e:
            await event.respond(f"Wrong password! Try again in a moment.{e}")
            await new_client.disconnect()
            return
    except Exception as e:
        await event.respond(f"Oops! That OTP doesn’t seem right.{e}")
        await new_client.disconnect()
        return

    # Export the session string
    session_str = new_client.session.save()
    await event.respond(f"<blockquote><b>Session generated ✅</b></blockquote>\n<code>{session_str}</code>", parse_mode="html")
    await new_client.disconnect()

async def listen(client, chat_id):
    loop = asyncio.get_event_loop()
    future = loop.create_future()

    @client.on(events.NewMessage(chats=chat_id))
    async def handler(event):
        if event.text and event.text.startswith("/"):
            print("Command detected, exiting listener.")
        else:
            if not future.done():
                future.set_result(event.raw_text)
        client.remove_event_handler(handler)

    try:
        result = await asyncio.wait_for(future, timeout=300)
    except asyncio.TimeoutError:
        print("Timeout: No message received in 5 minutes.")
        result = None
        client.remove_event_handler(handler)

    return result