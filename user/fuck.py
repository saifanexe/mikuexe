import asyncio
import random



import asyncio

ascii_art = [
    ".ㅤㅤ          /´ /)",
    "               /¯ ../",
    "             /¯ ../",
    "          ./... ./",
    "      /´¯/' ...'/´¯`•¸ ",
    "     /'/.../... ./.../¨¯\\",
    "   ('(...´(... ....~/'...')|.",
    "    \\.......... .....\\     /",
    "       \\''.........._.•´/",
    "         \\ .........   /",
    "           \\ ......... |",
    "              \\  ..... |",
    "                 \\.... |",
    "                    \\ .|",
    "                     \\\\",
    "                       \\🗿 ",
    "                         |\\.",
    "                        /\\."
]

async def fuck_handle(client, event):
  for i in range(1, len(ascii_art) + 1):
    frame = "\n".join(ascii_art[:i])
    try:
      await event.edit(frame)
    except Exception as e:
      print("Error:", e)
      return



async def fuckyou_handle(client, event):
  await event.edit("ᶠᶸᶜᵏᵧₒᵤ!")
  
  


async def safe_edit(event, new_text):
    try:
        if event.text != new_text:
            await event.edit(new_text)
    except Exception as e:
      pass

async def wtf_handle(client, event):
    original_text = "What the fuck bruh.."
    glitch_chars = ['@', '#', '$', '%', '&', '*', '!', '?', '/', '\\', '+', '-', '~']

    words = original_text.split()

    def glitch_word(word, glitch_count=2):
        word_list = list(word)
        indices = random.sample(range(len(word_list)), min(glitch_count, len(word_list)))
        for i in indices:
            if word_list[i] not in [' ', '.', ',']:
                word_list[i] = random.choice(glitch_chars)
        return "".join(word_list)

    displayed_words = []

    for word in words:
        for _ in range(5):
            glitched = glitch_word(word, glitch_count=max(1, len(word)//2))
            temp_text = " ".join(displayed_words + [glitched])
            await safe_edit(event, temp_text)
        displayed_words.append(word)
        await safe_edit(event, " ".join(displayed_words))

    await safe_edit(event, original_text)
