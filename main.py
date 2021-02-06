import os
import discord

#working with api
import requests
#since the zen is json based
import json

#since bot will be choosing the message randomly
import random

#using replit database
from replit import db

#this is a connection to discord
print("running the program")

client = discord.Client()

#list of sad words
sad_words = ["sad", "depressed", "unhappy", "mad", "angry", "miserable", "depressing"]

starter_encouragements = ["Cheer up!", "Hang in there", "You are awesome"]


#making a function for getting the quotes

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")

  #convert this reponse to json
  json_data = json.loads(response.text)

  quote = json_data[0]['q'] + " -" + json_data[0]['a']

  return quote


#add custom messages to database
def update_encouragements(encouraging_message):
  #check if encouragements is a key in the database
  if "encouragements" in db.keys():
    #then get all the values encouragements key in the database 
    encouragements = db["encouragements"]

    #adding encouraging messages
    encouragements.append(encouraging_message)

    #updateing in the database
    db["encouragements"] = encouragements

    #if there aren't any encouragements in database

  else:
    db["encouragements"] = [encouraging_message]

    
#to delete encouragements

def delete_encouragement(index):
  #getting list of the encouragements
  encouragements = db["encouragements"]
  #to make sure that the index is a part of the list and not more than that 
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements
#to register an event
#client uses events
@client.event


#this is an asynchronous lib
#using callbacks
#this event is called when the bot is ready to start being used
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

  #the 0.user gives us the username


  #another event to receive a message

@client.event
async def on_message(message):
  #dont do anything if the message is from the bot itself
  if message.author == client.user: 
    return

  #changing message.content to msg
  msg = message.content
  #not in order to let the bot know that a command is given, we will use: $hello
  if msg.startswith('$hello'):
    #once the bot knows that it received a command, it should return something
    #code to return message back to discord

    await message.channel.send('Hello there!' )

    #now to run the bot
    #pass the token as paramter

    #env is used to hide the token

  if msg.startswith('$inspire'):
    quote_disp = get_quote()
    await message.channel.send(quote_disp)


  #use encouragements from the database
  #using the previously created functions

  options = starter_encouragements

  #checking encouragements present database 
  if "encouragements" in db.keys():
    options = options + db["encouragements"]


  #adding more encouragements to the already assigned encouragements
  options = starter_encouragements
  if "encouragements" in db.keys():
    options = options + db["encouragements"]


  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ", 1)[1]
    #second element in the array is the new message

    #updating the encouragement

    update_encouragements(encouraging_message)

    await message.channel.send("New encouraging message added!")

  #to delete encouraging message

  if msg.startswith("$del"):
    #creating empty list
    encouragements = []
    #checking if encouragements in database
    if "encouragements" in db.keys():
      #then lets get the index
      index = int(msg.split("$del", 1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)
    #the empty list has been created since if there are no encouragements in the database, then the empty list is returned otherwise encouragements variable is unassigned
  #accessing all the messages in the discord chat

  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(options))
client.run(os.getenv('TOKEN'))