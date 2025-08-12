import requests
from config import FIREBASE





async def help_handle(client, event):
  await event.edit("Fetching commands...")
  cmd = fetch_commands()
  if cmd == False:
    await event.edit("Error fetching commands.")
    return
  
  if cmd == None:
    await event.edit("No data found.")
    return
  
  msg = format_commands(cmd)
  
  await event.edit(f"<blockquote>{msg}</blockquote>", parse_mode="html")
  
  





def format_commands(cmd: dict) -> str:
    if not cmd:
        return ""
    
    lines_count = len(cmd)
    
    # Define fixed width for box content (adjust as needed)
    box_width = 20
    
    # Top border
    result = "╔" + "═" * box_width + "╗\n"
    
    # Format each line
    for key, desc in cmd.items():
        key_part = f"//{key}"
        # max length of key part + 3 spaces for separator + desc
        # left align key_part to 12 chars, desc to fill rest
        key_str = key_part.ljust(12)
        desc_str = desc.ljust(box_width - 3 - 12)
        result += f"║ {key_str}: {desc_str} \n"
    
    # Bottom border
    result += "╚" + "═" * box_width + "╝"
    
    return result
    


def fetch_commands():
    url = f"{FIREBASE}/commands.json"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data is None:
            return None  # No data found
        
        # Agar 'commands' key exist karti hai to uske andar ka dict return karo
        if 'commands' in data:
            return data['commands']
        
        # Otherwise pura data hi return karo
        return data
    except Exception as e:
        return False
