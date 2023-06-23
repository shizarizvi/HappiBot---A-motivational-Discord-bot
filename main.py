import os
import discord
import requests
import json
import random
from replit import db

intent = discord.Intents.default()
intent.members = True
intent.message_content = True

client = discord.Client(intents=intent)

sadwords = ['sad','unhappy','depressed','feeling down','sorrowful','angry','miserable','bad day','die']

starter_enc = [
  'Cheer up buddy!!',
  'Koi baat nahi bestie, hota hai :))',
  'Zindagi hai, chalti rahe gi...',
  "'Verily, surely with hardship comes ease' (Quran 94:5)",
  "Don't worry, just partaiiiiiiiiii",
]


def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote= json_data[0]['q']+" ~"+json_data[0]['a']
  return quote

def update_encouragemnts(encouraging_message):
  if 'enc' in db.keys():
    enc = db["enc"]
    enc.append(encouraging_message)
    db["enc"]= enc

  else:
    db["enc"]= [encouraging_message]

def delete_encouragement(index):
  enc = db["enc"]
  if len(enc)>index:
    del enc[index]
    db["enc"]= enc

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('%hello'):
    await message.channel.send("Heyy :)")

  if message.content.startswith('%inspire'):
    quote=get_quote()
    await message.channel.send(quote)

  msg=message.content
  options = starter_enc
  if 'enc' in db.keys():
    options+=db['enc']

  if any(word in msg for word in sadwords):
    await message.channel.send(random.choice(options))

  if message.content.startswith('%new'):
    encouraging_message = msg.split('%new ',1)[1]
    update_encouragemnts(encouraging_message)
    await message.channel.send("New encouraging message added! Thanks bestie :))")

  if message.content.startswith("% del"):
    enc=[]
    if 'enc' in db.keys():
      index = int(msg.split('%del',1)[1])
      delete_encouragement(index)
      enc= db["enc"]
    await message.channel.send('The encouraging message: ""'+enc+'" has been deleted.')
      
    
  

client.run(os.getenv('token'))

