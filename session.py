
import time

active_users = set()
userbot = {}
users = {}
ping = {}
clone_users = {}

def client_users(me):
  user_id = me.id
  first_name = me.first_name
  username = me.username
  phone = me.phone
  
  users[user_id] = {
    "first_name" : first_name,
    "username" : username,
    "user_id" : user_id,
    "phone" : phone
  }


def set_ping():
  ts = int(time.time())
  ping["time"] = ts
  print("Ping has been set.")