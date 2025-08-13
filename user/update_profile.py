from telethon.tl.functions.account import UpdateProfileRequest
import asyncio
from telethon.tl.functions.photos import UploadProfilePhotoRequest
import os




async def setname(client, event):
    text = event.raw_text
    parts = text.split(maxsplit=1)
    command = parts[0] if len(parts) > 0 else ''
    name = parts[1] if len(parts) > 1 else None
    
    if not name:
        await event.edit("Provide Name after command.")
        return
    
    try:
        await client(UpdateProfileRequest(
        first_name=name
        ))
        await event.edit("Profile name has been changed ✅")
    except Exception as e:
        await event.edit(f"Please provide a valid Telegram profile name.")
    
    
    
async def setbio(client, event):
    text = event.raw_text
    parts = text.split(maxsplit=1)
    command = parts[0] if len(parts) > 0 else ''
    bio = parts[1] if len(parts) > 1 else None
    
    if not bio:
        await event.edit("Provide bio after command.")
        return
    
    await event.edit("Updating profile photo...")
    
    
    try:
        await client(UpdateProfileRequest(
        about=bio
        ))
        await event.edit("Profile bio has been changed ✅")
    except Exception as e:
        e = str(e)
        if "The provided bio is too long" in e:
            await event.edit("The provided bio is too long.")
            
        else:    
            await event.edit(f"Not a valid bio.")
        
        
        
        
async def setpfp(client, event):
    
    photo = None
    sender_id = event.sender_id
    
    if not event.is_reply:
        if event.photo:
            photo = event.photo
        else:
            photo = None
    else:
        reply_msg = await event.get_reply_message()
        if reply_msg.photo:
            photo = reply_msg.photo
        else:
            photo = None  
    
    if not photo:
        await event.edit("Reply or send a message containing a photo.")  
        return
    
    file_path = await client.download_media(photo, file=f'{sender_id}.jpg')    
    
    try:
        await client(UploadProfilePhotoRequest(file=await client.upload_file(file_path)))
        await event.edit("Profile photo has been changed ✅")
    except Exception as e:
        await event.edit(f"{e}")   
        
    if os.path.exists(file_path):
        os.remove(file_path)     