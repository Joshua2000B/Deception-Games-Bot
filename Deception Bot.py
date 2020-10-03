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
                if("cancel" in content):
                    return True
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
        mapping = {}
        x = 1
        for member in current_members:
            mapping[x] = member
            players[member] = copy.pop()
            embed = discord.Embed(title="You are a " + players[member].upper()+"!")
            img = discord.File("img/werewolf/"+players[member]+".png",players[member]+".png")
            embed.set_image(url="attachment://"+players[member]+".png")
            embed.add_field(name="Description",value=WEREWOLF_GOALS[players[member]])
            await member.send(file=img,embed=embed)
            x += 1
        player_static = players.copy()
        
        center = {"left":copy.pop(),"middle":copy.pop(),"right":copy.pop()}
        
        #Game Logic
        await message.channel.send("Everyone... go to sleep... (check your DMs for the roles. Your game will start in 10 seconds)")
        print("BEFORE:")
        for x in players:
            print(str(x) + " : " + players[x])
        print("MIDDLE:",center)
        await asyncio.sleep(10)

        # WEREWOLF LOGIC
        werewolves = tuple(x for x in player_static if player_static[x] == "werewolf")
        #print(werewolves)
        if(len(werewolves) == 0):
            print("No werewolves")
        elif(len(werewolves) == 1):
            await werewolves[0].send("There are no other Werewolves. Reply with `L`, `M`, or `R` to view a card from the center.")
            def check(msg):
                if(msg.author == werewolves[0] and type(msg.channel) == discord.DMChannel):
                    if(msg.content.lower() == "l"):
                        return True
                    elif(msg.content.lower() == "m"):
                        return True
                    elif(msg.content.lower() == "r"):
                        return True
                    else:
                        asyncio.get_event_loop().create_task(member.send("Invalid response."))
                        return False
                return False
            pick_message = await self.wait_for("message",check=check)
            pick = center[{"l":"left","m":"middle","r":"right"}[pick_message.content.lower()]]
            embed = discord.Embed(title="The card "+{"l":"on the left","m":"in the middle","r":"on the right"}[pick_message.content.lower()]+" is currently:")
            img = discord.File("img/werewolf/"+pick+".png",pick+".png")
            embed.set_image(url="attachment://"+pick+".png")
            await werewolves[0].send(file=img,embed=embed)
        elif(len(werewolves) == 2):
            # Maybe add an embed of the user's pfp
            await werewolves[0].send("Your Werewolf partner is "+str(werewolves[1])+".")
            await werewolves[1].send("Your Werewolf partner is "+str(werewolves[0])+".")

        # MINION LOGIC
        minion = tuple(x for x in player_static if player_static[x] == "minion")
        if(len(minion) == 0):
            print("No minion")
        elif(len(minion) == 1):
            await minion[0].send("There are no Werewolves among the players." if len(werewolves) == 0 else ("Your werewolf master(s) are:\n"+"\n".join([str(x) for x in werewolves])))

        # MASON LOGIC
        masons = tuple(x for x in player_static if player_static[x] == "mason")
        if(len(masons) == 0):
            print("No masons")
        elif(len(masons) == 1):
            await masons[0].send("There are no other Masons.")
        elif(len(masons) == 2):
            await masons[0].send("Your Mason partner is "+str(masons[1])+".")
            await masons[1].send("Your Mason partner is "+str(masons[0])+".")

        # SEER LOGIC
        seer = tuple(x for x in player_static if player_static[x] == "seer")
        if(len(seer) == 0):
            print("No seer")
        elif(len(seer) == 1):
            x = 0
            text = "\n```"
            for player in players:
                x += 1
                if(players == seer[0]):
                    continue
                text += str(x)+" : "+str(player)+"\n"
            text += "L : Left\nM : Middle\nR : Right```"
            await seer[0].send("Whose card would you like to look at? Type the number of the player you want to view the current card of (i.e., type `1` to view Player 1. You can also choose to view 2 cards of the center (i.e., type `L M` to view the Left and Middle)."+text)
            
            def check(msg):
                if(msg.author == seer[0] and type(msg.channel) == discord.DMChannel):
                    try:
                        response = int(msg.content)
                        if(response <= len(players) and response >= 0):
                            return True
                        else:
                            asyncio.get_event_loop().create_task(seer[0].send("Invalid response."))
                            return False
                    except:
                        response = msg.content.lower().split()
                        if(len(response) != 2):
                            asyncio.get_event_loop().create_task(seer[0].send("Invalid response."))
                            return False
                        if(response[0] in ["l","m","r"] and response[1] in ["l","m","r"] and response[0] != response[1]):
                            return True
                        else:
                            asyncio.get_event_loop().create_task(seer[0].send("Invalid response."))
                            return False
                return False
            seer_msg = await self.wait_for("message",check=check)
            try:
                checked_role = players[mapping[int(seer_msg.content)]]
                embed = discord.Embed(title=str(mapping[int(seer_msg.content)])+" is a:")
                img = discord.File("img/werewolf/"+checked_role+".png",pick+".png")
                embed.set_image(url="attachment://"+checked_role+".png")
                await seer[0].send(file=img,embed=embed)
            except:
                for x in range(seer_msg.content.lower().split()):
                    role = center[{'l':'left','m':'middle','r':'right'}[x]]
                    embed = discord.Embed(title="The card on the "+{'l':'left','m':'middle','r':'right'}[x]+"is:")
                    img = discord.File("img/werewolf/"+role+".png",pick+".png")
                    embed.set_image(url="attachment://"+role+".png")
                    await seer[0].send(file=img,embed=embed)

        # ROBBER LOGIC
        robber = tuple(x for x in player_static if player_static[x] == "robber")
        if(len(robber) == 0):
            print("No robber")
        elif(len(robber) == 1):
            x = 0
            text = "\n```"
            for player in players:
                x += 1
                if(players == robber[0]):
                    continue
                text += str(x)+" : "+str(player)+"\n"
            text += "```"
            await robber[0].send("Whose card would you like to steal? Type the number of the player you want to steal the current card of (i.e., type `1` to steal Player 1."+text)
            def check(msg):
                if(msg.author == robber[0] and type(msg.channel) == discord.DMChannel):
                    try:
                        response = int(msg.content)
                        if(response <= len(players) and response >= 0):
                            return True
                        return False
                    except:
                        asyncio.get_event_loop().create_task(robber[0].send("Invalid response."))
                        return False
                return False
            robber_msg = await self.wait_for("message",check=check)
            swap_player = mapping[int(robber_msg.content)]
            players[robber[0]], players[swap_player] = players[swap_player], players[robber[0]]
            embed = discord.Embed(title="Your new card is:")
            img = discord.File("img/werewolf/"+players[robber[0]]+".png",pick+".png")
            embed.set_image(url="attachment://"+players[robber[0]]+".png")
            await seer[0].send(file=img,embed=embed)

        # TROUBLEMAKER LOGIC
        troublemaker = tuple(x for x in player_static if player_static[x] == "troublemaker")
        if(len(troublemaker) == 0):
            print("No troublemaker")
        elif(len(troublemaker) == 1):
            x = 0
            text = "\n```"
            for player in players:
                x += 1
                if(players == robber[0]):
                    continue
                text += str(x)+" : "+str(player)+"\n"
            text += "```"
            await robber[0].send("Select the 2 people whose cards you would like to swap? Type the numbers of the players you want to swap the current cards of (i.e., type `2 4` to swap Player 2 with Player 5."+text)
            def check(msg):
                if(msg.author == troublemaker[0] and type(msg.channel) == discord.DMChannel):
                    numbers = msg.content.split()
                    if(len(numbers) == 2):
                        try:
                            if(int(numbers[0]) <= len(players) and int(numbers[0]) >= 0 and int(numbers[1]) <= len(players) and int(numbers[1]) >= 0 and numbers[0] != numbers[1]):
                                return True
                            asyncio.get_event_loop().create_task(troublemaker[0].send("Invalid response."))
                            return False
                        except:
                            asyncio.get_event_loop().create_task(troublemaker[0].send("Invalid response."))
                            return False
                    asyncio.get_event_loop().create_task(troublemaker[0].send("Invalid response."))
                    return False
                return False
            troublemaker_msg = await self.wait_for("message",check=check)
            swap1, swap2 = [mapping[int(x)] for x in troublemaker_msg.content.split()]
            players[swap1], players[swap2] = players[swap2], players[swap1]
            await message.channel.send(str(swap1)+" and "+str(swap2)+" have been swapped.")

        # DRUNK LOGIC
        drunk = tuple(x for x in player_static if player_static[x] == "drunk")
        if(len(drunk) == 0):
            print("No drunk")
        elif(len(drunk) == 1):
            await drunk[0].send("Select a card from the middle you would like to swap with. You can choose from `L` for the left, `M` for the middle, and `R` for the Right.")
            def check(msg):
                if(msg.author == drunk[0] and type(msg.channel) == discord.DMChannel):
                    if(msg.content.lower() in ["l","m","r"]):
                        return True
                    else:
                        asyncio.get_event_loop().create_task(drunk[0].send("Invalid response."))
                        return False
                return False
            drunk_msg_content = self.wait_for("message",check=check).content.lower()
            players[drunk[0]], center[{'l':"left",'m':"middle",'r':"right"}[drunk_msg_content]] = center[{'l':"left",'m':"middle",'r':"right"}[drunk_msg_content]], players[drunk[0]]
            await drunk[0].send("You have swapped with the "+{'l':"left",'m':"middle",'r':"right"}[drunk_msg_content]+" card.")

        # INSOMNIAC LOGIC
        insomniac = tuple(x for x in player_static if player_static[x] == "insomniac")
        if(len(insomniac) == 0):
            print("No insomniac")
        elif(len(insomniac) == 1):
            embed = discord.Embed(title="You ended the night as:")
            img = discord.File("img/werewolf/"+players[insomniac[0]]+".png",pick+".png")
            embed.set_image(url="attachment://"+players[insomniac[0]]+".png")
            await seer[0].send(file=img,embed=embed)


        print("AFTER:")
        for x in players:
            print(str(x) + " : " + players[x])
        print("MIDDLE:",center)
            
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
