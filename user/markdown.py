



async def markdown_handle(client, event):
  text = event.raw_text
  sender_id = event.sender_id
  if not text:
    return
  
  msg = blockquote(text)
  if not msg:
    return
  await event.edit(msg, parse_mode="html")






def blockquote(text: str) -> str:
    lines = text.split('\n')
    
    # Check agar koi line > se start hoti hai ya nahi
    if not any(line.startswith('>') for line in lines):
        return None

    msg_lines = []
    blockquote_lines = []

    def flush_blockquote():
        if blockquote_lines:
            msg_lines.append("<blockquote>" + "\n".join(blockquote_lines) + "</blockquote>")
            blockquote_lines.clear()

    for line in lines:
        if line.startswith('>'):
            # Remove leading '> ' ya '>' 
            cleaned = line.lstrip('> ').rstrip()
            blockquote_lines.append(cleaned)
        else:
            flush_blockquote()
            msg_lines.append(line)

    flush_blockquote()
    return "\n".join(msg_lines)