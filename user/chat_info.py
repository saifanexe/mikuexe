from telethon.tl.types import ChannelParticipantsAdmins
from telethon.tl.functions.messages import EditChatTitleRequest



async def get_admins(client, event):
    if event.is_private:
        await event.edit("Try on group chats.")
        return
        
    chat_id = event.chat_id   
    
    admins = []
     
    async for user in client.iter_participants(chat_id, filter=ChannelParticipantsAdmins):
        if not user.bot:  # bots ko skip karo
            admins.append({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username
            })
            
    msg = ""  # empty string to start
    for admin in admins:
        name = admin['first_name']
        user_id = admin['id']
        msg += f"➠ <a href='tg://user?id={user_id}'>{name}</a>\n"
    
    await event.edit(f"{msg}", parse_mode="html")    
    
    

async def tag_admins(client, event):
    if event.is_private:
        await event.edit("Try on group chats.")
        return
        
    chat_id = event.chat_id   
    
    admins = []
     
    async for user in client.iter_participants(chat_id, filter=ChannelParticipantsAdmins):
        if not user.bot:  # bots ko skip karo
            admins.append({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username
            })
            
    msg = "@admins"  # empty string to start
    for admin in admins:
        name = admin['first_name']
        user_id = admin['id']
        msg += f"<a href='tg://user?id={user_id}'>.</a>"
    
    await event.delete()
    await event.respond(f"{msg}", parse_mode="html")
    
    
