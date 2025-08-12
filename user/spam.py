import asyncio


async def spam_handle(client, event):
  text = event.raw_text
  parts = text.split(maxsplit=2)
  command = parts[0]      
  times = parts[1] if len(parts) > 1 else None
  value = parts[2] if len(parts) > 2 else ""
  
  if not times:
    await event.edit("`//spam 10 message`")
    return
  
  try:
    times = int(times)
  except:
    await event.edit("The second argument must be an integer.")
    return
  
  if not value:
    await event.edit("The message cannot be empty.")
    return
  
  await event.delete()
  
  for i in range(times):
    await event.respond(f"{value}")
    