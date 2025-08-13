from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.account import UpdateProfileRequest
import asyncio
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from telethon.tl.functions.photos import DeletePhotosRequest
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest
import os

import os
from session import clone_users, users


async def clone_user(client, event):
    
    user = None
    sender_id = event.sender_id
    
    if event.is_private:
        user = event.chat_id
        
    elif event.is_reply:
        reply_msg = await event.get_reply_message()
        user = reply_msg.sender_id
        
    else:
        text = event.raw_text
        parts = text.split(maxsplit=1)
        command = parts[0] if len(parts) > 0 else ''
        user = parts[1] if len(parts) > 1 else None     
        
        
    if not user:
        await event.edit("Reply or provide username after command.")   
        return
        
    try:
        userinfo = await client(GetFullUserRequest(user))
        user = userinfo.users[0]
    except Exception as e:
        await event.edit(f"{e}")  
        return
        
    first_name = user.first_name
    user_id = user.id
    profile = bool(user.photo) 
    mention = f"<a href='tg://user?id={user_id}'>{first_name}</a>"
    file_path = None
    
    await event.edit(f"{mention}'s profile is being cloned...", parse_mode="html")
    
    if profile:
        
        try:
            file_path = await client.download_profile_photo(user_id, file=f"{user.id}.jpg")
            await client(UploadProfilePhotoRequest(file=await client.upload_file(file_path)))
        except Exception as e:
            await event.edit(f"{e}")   
            return
            
            
    try:         
        await client(UpdateProfileRequest(
        first_name=first_name
        ))   
    except Exception as e:
        await event.edit(f"{e}")   
        return 
        
    await event.edit(f"{mention}'s profile has been cloned ✅", parse_mode="html")
    
    if file_path:
        if os.path.exists(file_path):
            os.remove(file_path) 
    
    # Ensure the list exists
    if sender_id not in clone_users:
        clone_users[sender_id] = []

    # Append default data
    clone_users[sender_id].append({
        "first_name": first_name,
        "user_id" : user_id,
        "profile": profile
    })    
        
        
        
        

async def revert_user(client, event):
    
    sender_id = event.sender_id
    first_name = None
    user_id = None
    profile = None
    me = None
    mention = None
    
    
    current, pre = clone_data(sender_id)
    
    if not current and not pre:
        await event.edit("There is no cloned user left.")
        return
        
    if current and not pre:
        data = users.get(sender_id,{})
        if not data:
            await event.edit(f"{data}")
            return
        #my original data
        first_name = data.get("first_name")
        user_id = data.get("user_id")
        #previous profile info
        profile = current.get("profile")
        me = True
        await event.edit(f"Reverting to your original account...", parse_mode="html")
        
        
    if current and pre:
        #previous user data
        first_name = pre.get("first_name")
        user_id = pre.get("user_id") 
        me = False
        #current profile photo info
        profile = current.get("profile")
        mention = f"<a href='tg://user?id={user_id}'>{first_name}</a>"
        await event.edit(f"Reverting to {mention}'s account...", parse_mode="html")
        
        
        
    if profile:
        is_deleted = await delete_profile_photo(client)   
        
    await client(UpdateProfileRequest(
        first_name=first_name
        ))    
        
    if me:
        await event.edit("Your original account has been restored ✅")
    else:    
        await event.edit(f"{mention}'s account has been reverted ✅", parse_mode="html")
        
        
async def delete_profile_photo(client):
    photos = await client(GetUserPhotosRequest(
        user_id='me',
        offset=0,
        max_id=0,
        limit=1
    ))
    if photos.photos:
        await client(DeletePhotosRequest(id=[photos.photos[0]]))
        return True
    return False        
        

def clone_data(sender_id):
    data_list = clone_users.get(sender_id, [])

    if len(data_list) == 0:
        return None, None
    elif len(data_list) == 1:
        data = data_list.pop(0)
        return data, None
    else:
        last = data_list.pop(-1)
        second_last = data_list[-1]  # last item
        return last, second_last        