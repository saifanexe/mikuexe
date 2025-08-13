import asyncio
import random




text1 = "ɪ ʟᴏᴠᴇ ʏᴏᴜᴜᴜ 💖"
heart = ['💞', '💓', '💘', '💝', '💖']
text2 = "ʟᴏᴠᴇ ʏᴏᴜ 💘💞💖"
f = ["ɪ"," ʟᴏᴠᴇ"," ʏᴏᴜ"," ғᴏʀᴇᴠᴇʀ 💖"]
b = ["ɪ", " ʟᴏᴠᴇ", " ʏᴏᴜ", " ʙᴀʙʏ 💖"]
ily = "ʟᴏᴠᴇ ʏᴏᴜ ᴄᴜᴛᴇ sɪ ᴊᴀᴀɴ 💖"



async def lover_handle(client, event):
  anim = 30
  space = "\u200B"
  for i in range(anim):
    random_hearts = random.sample(heart, 4)
    text = "".join(random_hearts)
    if i == 10:
      for s in f:
        await event.edit(f"{s}")
        await asyncio.sleep(1)
    elif i == 20:
      for s in b:
        await event.edit(f"{s}")
        await asyncio.sleep(1)
    else:
      await event.edit(text+space)
    
  await event.edit(ily)
  
  
