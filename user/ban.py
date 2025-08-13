from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights






async def ban_handle(client, event):
    
    text = event.raw_text
    parts = text.split(maxsplit=1)
    command = parts[0] if len(parts) > 0 else ''
    full_value = parts[1] if len(parts) > 1 else None
    text_value = full_value.split(maxsplit=1)[0] if full_value else None
    text_reason = full_value.split(maxsplit=1)[1] if full_value and len(full_value.split(maxsplit=1)) > 1 else None
    
    
    if event.is_private:
        await event.edit("Try on group chats.")
        return
        
    if event.is_reply:
        reply = await event.get_reply_message()
        value = reply.sender_id
        reason = full_value
        
    else:
        if not text_value:
            await event.edit("Reply to a user or provide a username.")
            return
            
        value = text_value
        reason = text_reason   
         
    await ban_user(client, event, value, reason)
    
    





async def ban_user(client, event, user, reason):
    rights = ChatBannedRights(
        until_date=None,     
        view_messages=True     
    )
    try:
        await client(EditBannedRequest(
            channel=event.chat_id,
            participant=user,
            banned_rights=rights
        ))
        user = await client.get_entity(user)
        first_name = user.first_name
        user_id = user.id
        
        if reason:
            mention = f'<a href="tg://user?id={user_id}">{reason}</a>'
            await event.edit(f"{mention}", parse_mode="html")
        else:
            await event.delete()   
        
    except Exception as e:
        e = str(e)
        if "Chat admin privilege" in e:
            await event.edit("Oops! Looks like I'm not an admin.")
            
        elif "Either you're not an admin or you tried to ban an admin" in e:
            await event.edit("Nope, I can't ban an admin.")   
            
        else:
            await event.edit("Who the heck is this?")  
            
            
            
            
            








async def unban_handle(client, event):
    
    text = event.raw_text
    parts = text.split(maxsplit=1)
    command = parts[0] if len(parts) > 0 else ''
    full_value = parts[1] if len(parts) > 1 else None
    text_value = full_value.split(maxsplit=1)[0] if full_value else None
    text_reason = full_value.split(maxsplit=1)[1] if full_value and len(full_value.split(maxsplit=1)) > 1 else None
    
    
    if event.is_private:
        await event.edit("Try on group chats.")
        return
        
    if event.is_reply:
        reply = await event.get_reply_message()
        value = reply.sender_id
        reason = full_value
        
    else:
        if not text_value:
            await event.edit("Reply to a user or provide a username.")
            return
            
        value = text_value
        reason = text_reason   
         
    await unban_user(client, event, value, reason)
    
    





async def unban_user(client, event, user, reason):
    rights = ChatBannedRights(
        until_date=None,     
        view_messages=False     
    )
    try:
        await client(EditBannedRequest(
            channel=event.chat_id,
            participant=user,
            banned_rights=rights
        ))
        user = await client.get_entity(user)
        first_name = user.first_name
        user_id = user.id
        
        if reason:
            mention = f'<a href="tg://user?id={user_id}">{reason}</a>'
            await event.edit(f"{mention}", parse_mode="html")
        else:
            await event.delete()   
        
    except Exception as e:
        e = str(e)
        if "Chat admin privilege" in e:
            await event.edit("Oops! Looks like I'm not an admin.")
            
        elif "Either you're not an admin or you tried to ban an admin" in e:
            await event.edit("Nope, I can't unban an admin.")   
            
        else:
            await event.edit("Who the heck is this?")              