from telethon import events
from user.spam import spam_handle
from user.love import loveyou_handle, love_handle
from user.fuck import fuck_handle, wtf_handle, fuckyou_handle
from user.type import type_handle
from user.markdown import markdown_handle
from user.afk import afk_handle, afkmsg_handle, stop_afk
from user.afk import afk_handle, afkmsg_handle, stop_afk
from user.lover import lover_handle
from user.dino import dino_anim
from user.nah import nah_handle
from user.brain import brain_handle
from user.wtf import wtf_handle
from user.bomb import bomb_handle
from bot.ping import ping_handle

def register(client):
  @client.on(events.NewMessage(outgoing=True, pattern=r'^//ping(?:\s+(.*))?$'))
  async def ping(event):
    await ping_handle(client, event)
    
  @client.on(events.NewMessage(outgoing=True, pattern=r'^//bomb(?:\s+(.*))?$'))
  async def bomb(event):
    await bomb_handle(client, event)
    
  @client.on(events.NewMessage(outgoing=True, pattern=r'^//brain(?:\s+(.*))?$'))
  async def brain(event):
    await brain_handle(client, event)
  
  @client.on(events.NewMessage(outgoing=True, pattern=r'^//wtf(?:\s+(.*))?$'))
  async def wtf(event):
    await wtf_handle(client, event)
    
  @client.on(events.NewMessage(outgoing=True, pattern=r'^//nah(?:\s+(.*))?$'))
  async def nah(event):
    await nah_handle(client, event)
    
  @client.on(events.NewMessage(outgoing=True, pattern=r'^//dino(?:\s+(.*))?$'))
  async def dino(event):
    await dino_anim(client, event)
    
  @client.on(events.NewMessage(outgoing=True, pattern=r'^//lover(?:\s+(.*))?$'))
  async def lover(event):
    await lover_handle(client, event)
    
  @client.on(events.NewMessage(outgoing=True, pattern=r'^//afk(?:\s+(.*))?$'))
  async def afk(event):
    await afk_handle(client, event)
    
  @client.on(events.NewMessage(outgoing=True, pattern=r'^//type(?:\s+(.*))?$'))
  async def type(event):
    await type_handle(client, event)
  
  @client.on(events.NewMessage(outgoing=True, pattern=r'^//fuckyou(?:\s+(.*))?$'))
  async def fuckyou(event):
    await fuckyou_handle(client, event)

  @client.on(events.NewMessage(outgoing=True, pattern=r'^//fuck(?:\s+(.*))?$'))
  async def fuck(event):
    await fuck_handle(client, event)
    
  @client.on(events.NewMessage(outgoing=True, pattern=r'^//love(?:\s+(.*))?$'))
  async def love(event):
    await love_handle(client, event)
    
  @client.on(events.NewMessage(outgoing=True, pattern=r'^//loveyou(?:\s+(.*))?$'))
  async def loveyou(event):
    await loveyou_handle(client, event)
    
  @client.on(events.NewMessage(outgoing=True, pattern=r'^//spam(?:\s+(.*))?$'))
  async def spam(event):
    await spam_handle(client, event)
  
  @client.on(events.NewMessage(outgoing=True))
  async def markdown(event):
    await markdown_handle(client, event)
    await stop_afk(client, event)
  
  @client.on(events.NewMessage(incoming=True))
  async def afk_msg(event):
    await afkmsg_handle(client, event)