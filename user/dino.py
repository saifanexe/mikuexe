


text1 = "ᴅɪɴ ᴅɪɴɴɴ..."
text2 = "ᴅɪɴᴏᴏᴏᴏᴏᴜꜱᴏᴜʀꜱꜱꜱ.... "
text3 = "ʜᴇ ᴡᴀꜱ ɢᴇᴛᴛɪɴɢ ᴄʟᴏꜱᴇʀ!"
text4 = "ᴊᴜꜱᴛ ɢɪᴠᴇ ᴜᴘ "
text5 = "-ᴅɪᴇᴅ-"
man = "🏃🏻"
g_man = "🧎🏻"
dino = "🦖"

import asyncio
async def dino_anim(client, event):
  zwsp = "\u200B"
  await event.edit(text1)
  await asyncio.sleep(1.5)
  await event.edit(text2)
  await asyncio.sleep(0.5)
  gap_total = 50
  for i in range(gap_total):
    gap = gap_total - i
    msg = man + " "*gap + dino
    if i == 25:
      await event.edit(text3)
      await asyncio.sleep(1.5)
    elif i == 35:
      await event.edit(text4)
      await asyncio.sleep(1.5)
    else:
      await event.edit(f"{msg}{zwsp}")
  
  await event.edit(f"{g_man}{dino}{zwsp}")
  await asyncio.sleep(0.5)
  await event.edit(text5)