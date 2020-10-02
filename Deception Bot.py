#https://discordpy.readthedocs.io/en/latest/api.html
#API for Discord.py


import discord
import asyncio
from datetime import *
import random

WEREWOLF_GOALS = {
    "werewolf":"Your goal is to survive the night! If at least 1 Werewolf dies, the Werewolf team loses! Use deception to trick your enemies into believeing you are innocent.",
    "minion":"You are a villager that has been brainwashed by the Werewolves! Help them win by decieving your enemies! You win if the Werewolves win.",
    "mason":"The Masons are a close group that always look out for each other. At night, you get to look for your Mason brother. You are on the side of the villagers.",
    "seer":"You are a magical Seer that can peer into the true intentions on a person. At night, you get to look at the indentity of a person. You are on the side of the villagers.",
    "robber":"You are a thief who skulks about in the night. At night, you get to swap roles with 1 other player, and then look at your new card. You are on the side of the villagers.",
    "troublemaker":"You are the town's Troublemaker, and you love to cause mischief. At night, you switch two other players' cards. You are on the side of the villagers.",
    "drunk":"Every night, you get so drunk you can't even remember who you are. You swap your card with a card from the center, but do not look at it. You are on the side of the villagers.",
    "insomniac":"You have trouble staying alseep all night. At the very end of the night, you wake up and get to check your card again. You are on the side of the villagers.",
    "tanner":"You hate your job so much and want to die. If you are killed at the end of the game, you and only you win the game. You cna only win in this way.",
    "hunter":"You have quick reflexes in the face of death. If you die, whoever you voted for *also* dies. You are on the side of the villagers.",
    "villager":"You are a normal villager, and do nothing special during the night. You are on the side of the villagers."
    }


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
        #elif(command == "/test"):
            



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
        current_members = vc.members.copy()
        #print(vc)
        num_of_players = len(current_members)
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
Max of 1 Insomniac
Max of 2 Masons
Max of 1 Minion```
To choose the roles, send them as a space-separated list of the roles you want. For example, a valid response for 6 player game would be `seer tanner robber villager villager minion troublemaker`. You can also type `cancel` to cancel.""")
        valid = ("villager","seer","robber","troublemaker","tanner","drunk","hunter","insomniac","mason","minion","cancel")
        def check(msg):
            if(msg.author == message.author and msg.channel == message.channel):
                content = msg.content
                for role in content.lower().split():
                    if(role not in valid):
                        #await message.channel.send("Unrecognized role: "+role)
                        asyncio.get_event_loop().create_task(message.channel.send("Unrecognized role: "+role))
                        return False
                if(len(content.lower().split()) != num_of_roles - 2):
                    asyncio.get_event_loop().create_task(message.channel.send("Incorrect number of roles - you need "+str(num_of_roles - 2)+" roles."))
                    return False
                if(content.count("villager") > 3 or content.count("seer") > 1 or content.count("insomniac") > 1 or content.count("robber") > 1 or content.count("troublemaker") > 1 or content.count("tanner") > 1 or content.count("drunk") > 1 or content.count("hunter") > 1 or content.count("mason") > 2 or content.count("minion") > 1):
                    asyncio.get_event_loop().create_task(message.channel.send("You have too many of one or more roles. See above to check for the max of each role."))
                    return False
                return True
            return False
            
        try:
            roles_msg = await self.wait_for("message",check=check,timeout=120)
        except asyncio.TimeoutError:
            await message.channel.send("Game cancelled - there was no response for 2 minutes.")
            return
        if("cancel" in roles_msg.content):
            await message.channel.send("Game cancelled.")
            return
        roles = ["werewolf","werewolf"] + roles_msg.content.lower().split()
        copy = roles.copy()
        #print(roles)

##        embed = discord.Embed(title="Title",description="desc")
##        img = discord.File("img/werewolf/tanner.png","tanner.png")
##        embed.set_image(url="attachment://tanner.png")
##        embed.add_field(name="Fiel1", value="hi", inline=False)
##
##        await message.channel.send(file=img,embed=embed)

        players = {}
        random.shuffle(copy)
        for member in current_members:
            players[member] = copy.pop()
            embed = discord.Embed(title="You are a " + players[member].upper()+"!")
            img = discord.File("img/werewolf/"+players[member]+".png",players[member]+".png")
            embed.set_image(url="attachment://"+players[member]+".png")
            embed.add_field(name="Description",value=WEREWOLF_GOALS[players[member]])
            await member.send(file=img,embed=embed)

        center = {"left":copy.pop(),"center":copy.pop(),"right":copy.pop()}
        #print(players,center)
        
        #Game Logic
        await message.channel.send("Everyone... go to sleep... (check your DMs for the roles. Your game will start in 10 seconds)")
        #await asyncio.sleep(10)

        werewolves = tuple(x for x in players if players[x] == "werewolf")
        print(werewolves)
        if(len(werewolves) == 0):
            pass
        elif(len(werewolves

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
