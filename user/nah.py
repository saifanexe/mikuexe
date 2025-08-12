import asyncio

text1 = r"""(\_/)
(●_●)
/>💖* ᴛʜɪs ɪs ғᴏʀ ʏᴏᴜ """
text2 = r"""(\_/)
(●_●)"""


async def nah_handle(client, event):
  space = "\u200B"
  await event.edit(f"{space} {text1}")
  await asyncio.sleep(3)
  await event.edit(f"{space} {text2}")