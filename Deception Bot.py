#https://discordpy.readthedocs.io/en/latest/api.html
#API for Discord.py


import discord
import asyncio
from datetime import *


class MyClient(discord.Client):

    
    #ON MESSAGE
    async def on_message(self,message):
        if(message.content.startswith("/")):
            await self.process_commands(message)



    #PROCESS COMMANDS
    async def process_commands(self,message):
        command = message.content.split()[0].lower()
        #Command List Here
        if(command == "/play"):
            await self.play(message)



    async def play(self,message):
        command = message.content.split()
        if(len(command) == 1):
            await message.channel.send("""Here are my list of games! Type `/play <game>` to start one!```
Werewolf
```""")
            return
            
        elif(len(command) != 2):
            await message.channel.send("You didn't specify a game to play!")
            return

        elif(message.author.voice == None):
            await message.channel.send("You aren't in a voice channel!")
            return

        if(command[1].lower() == "werewolf"):
            await self.play_werewolf(message)


    async def play_werewolf(self,message):
        vc = message.author.voice.channel
        #print(vc)
        num_of_players = len(vc.members)
        #num_of_players = 8
        num_of_roles = num_of_players + 3
##        if(num_of_players < 5 or num_of_players > 12):
##            await message.channel.send("You do not have the correct number of people to play Werewolf. You need 5-12 Players to play.")
##            return
        await message.channel.send("Alright, you have "+str(num_of_players)+" players. Now, choose what roles to play with. Every game always has 2 Werewolves, so you need to pick "+str(num_of_roles-2)+""" other roles. You have your choice between:```
Max of 3 Villagers
Max of 1 Seer
Max of 1 Robber
Max of 1 Troublemaker
Max of 1 Tanner
Max of 1 Drunk
Max of 1 Hunter
Max of 2 Masons
Max of 1 Minion```
To choose the roles, send them as a space-separated list of the roles you want. For example, a valid response for 6 player game would be `seer tanner robber villager villager minion troublemaker`. You can also type `cancel` to cancel.""")
        valid = ("villager","seer","robber","troublemaker","tanner","drunk","hunter","mason","minion","cancel")
        def check(msg):
            if(msg.author == message.author and msg.channel == message.channel):
                content = msg.content
                for role in content.lower().split():
                    if(role not in valid):
                        #await message.channel.send("Unrecognized role: "+role)
                        asyncio.get_event_loop().create_task(message.channel.send("Unrecognized role: "+role))
                        return False
                if(content.count("villager") > 3 or content.count("seer") > 1 or content.count("robber") > 1 or content.count("troublemaker") > 1 or content.count("tanner") > 1 or content.count("drunk") > 1 or content.count("hunter") > 1 or content.count("mason") > 2 or content.count("minion") > 1):
                    asyncio.get_event_loop().create_task(message.channel.send("You have too many of one or more roles. See above to check for the max of each role."))
                    return False
                return True
            return False
            
        try:
            roles_msg = await self.wait_for("message",check=check,timeout=120)
        except asyncio.TimeoutError:
            await message.channel.send("Game cancelled - there was no response for 2 minutes.")
            return
        if(roles_msg.content == "cancel"):
            await message.channel.send("Game cancelled.")
            return
        roles = ["werewolf","werewolf"] + roles_msg.content.lower().split()
        print(roles)
        

    #WHEN READY
    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name = "/help"))
        print("Successfully set Bot's game status")


    #CONNECTION
    async def on_connect(self):
        print("Bot has connected to server at time:",datetime.now())
    
    #DISCONNECTION
    async def on_disconnect(self):
        print("Bot has disconnected from server at time:",datetime.now())



print("Starting Bot")
bot = MyClient()
file = open("TOKEN.txt",'r')
TOKEN = file.read()
#print(TOKEN)
bot.run(TOKEN)
