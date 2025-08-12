from telethon import functions, types

# Set status to offline (last seen a while ago)


afk_session = {}




async def afk_handle(client, event):
  
  sender_id = event.sender_id
  text = event.raw_text.strip()
  parts = text.split(' ', 1)
  command = parts[0]  
  value = parts[1] if len(parts) > 1 else ""  
  if not value:
    value = "I'm currently afk!"
  
  afk_session.setdefault(sender_id, value)
  await event.edit("Going AFK for a while. Will respond later.")



async def afkmsg_handle(client, event):
  me = await client.get_me()
  user_id = me.id
  
  if not event.is_private:
    if event.is_reply:
      reply_msg = await event.get_reply_message()
      reply_user = reply_msg.sender_id
      if reply_user == user_id:
        user_id = reply_user
    else:
      return
    
  afk_msg = afk_session.get(user_id)
  if not afk_msg:
    return
  
  await event.reply(afk_msg)
  try:
    await client(functions.account.UpdateStatusRequest(
    offline=True
    ))
  except Exception as e:
    print(e)
  


async def stop_afk(client, event):
  text = event.raw_text
  sender_id = event.sender_id
  if text:
    if text.startswith("//afk"):
      return
    
  if sender_id in afk_session:
    afk_session.pop(sender_id)