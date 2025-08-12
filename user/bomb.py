import asyncio

bomb = "💣"
square = "⬛"
blast = "💥"

async def bomb_handle(client, event):
    textb = bomb * 4
    texts = square * 5
    textbl = blast * 4
    
    frames = []
    
    # Start with all squares 5 lines
    frames.append("\n".join([texts]*5))
    
    # For 4 lines (0 to 3)
    for i in range(5):
        # Bomb frame on line i
        frame_lines = []
        for line_no in range(5):
            if line_no == i:
                frame_lines.append(textb)
            else:
                frame_lines.append(texts)
        frames.append("\n".join(frame_lines))
        
        # Blast frame on same line i
        frame_lines = []
        for line_no in range(5):
            if line_no == i:
                frame_lines.append(textbl)
            else:
                frame_lines.append(texts)
        frames.append("\n".join(frame_lines))
    
    # Finally all squares again (optional)
    frames.append("\n".join([texts]*5))
    
    # Animate all frames
    for frame in frames:
        await event.edit(frame)
        await asyncio.sleep(0.2)
    
    await event.edit("ʀɪᴘ ᴍᴀʀ ɢʏᴀ ʙsᴅᴋ😂😂......")
