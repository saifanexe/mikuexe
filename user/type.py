import asyncio





async def type_handle(client, event):
  
  command, value = event.text.split(' ', 1) if ' ' in event.text else (event.text, '')
  
  if value == "":
    await event.edit("Provide message after command")
    return
  
  val = len(value)
  
  if len(value) > 120:
    await event.edit("event is too long.")
    return
  
  cursor = "▌"
  text = value
  for i in range(1, len(value)):
    await event.edit(text[:i] + cursor)
  await event.edit(text)
  
  
  

