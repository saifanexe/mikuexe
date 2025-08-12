

text1 = "ʏᴏᴜʀ ʙʀᴀɪɴ ➠ 🧠"
text2 = "(> ^_^)>"
text3 = "<(^_^ <)"
brain = "🧠"
binn = "🗑️"

async def brain_handle(client, event):
  gap = 15
  for i in range(0, gap):
    g = gap - i
    msg = f"""{text1}
    
{brain} {" "*g}{text3}{" "*i}{binn}
"""
    await event.edit(msg)
  
  for i in range(0, gap):
    g = gap - i
    
    if i == gap-1:
      msg = f"""{text1}
      
{" "*i}{text2}{" "*g}{binn}
"""
    else:
      msg = f"""{text1}
      
{" "*i}{text2}{brain}{" "*g}{binn}
"""
    await event.edit(msg)
  