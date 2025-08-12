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
    result = ""
    for key, desc in cmd.items():
        result += f"//{key} : {desc}\n"
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