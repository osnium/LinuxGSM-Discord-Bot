import discord
from discord.ext import commands
from discord.commands import slash_command
from discord.commands import SlashCommandGroup
from discord import Option
import subprocess
import json

running = False
gameRunning = None
cmds = ["start", "stop", "restart", "update"]

with open("gameservers.json", "r") as f:
    global config
    config = json.load(f)

class gameservers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #get the Gameservers from the config file
    def get_servers(ctx: discord.AutocompleteContext):
        gameservers = list(config.keys())
        return gameservers

    #get the actions from the cmds list
    def get_cmds(ctx: discord.AutocompleteContext):
        return cmds


    #Starts, Stops, Restarts or Updates a Gameserver
    @slash_command(name = "server", description = "Starts, Stops, Restarts or Updates a Gameserver")
    async def server(self, ctx, server: Option(str, autocomplete=get_servers), action: Option(str, autocomplete=get_cmds), cmds):
        gameservers = list(config.keys())
        global running
        global gameRunning


        #Checks if the Server exists
        if server not in gameservers:
            await ctx.respond(f"The server {server} does not exist!, available servers are: {', '.join(gameservers)}")
            return
        
        #Checks if the action exists
        if action not in cmds:
            await ctx.respond(f"The action {action} does not exist!, available actions are: {', '.join(cmds)}")
            return

        #Starts the Server
        if action == "start":
            if running == True: #Checks if a Server is already running
                await ctx.respond(f"{gameRunning} is already running! Please stop it first!")
                return
            else: #Starts the Server
                serverFile = config[server]["path"]
                command = [config[server]["fileName"], action]
                process = subprocess.Popen(command, cwd=serverFile,)
                await ctx.respond(f"**{config[server]['serverName']}** is starting!")
                await self.bot.change_presence(status=None, activity=discord.Game(config[server]["serverName"]))
                running = True
                gameRunning = config[server]["serverName"]
                return running, gameRunning
            
        #stops the Server
        elif action == "stop":
            if running == False: #checks if a Server is running
                await ctx.respond("No Server is running!")
                return
            
            elif gameRunning != config[server]["serverName"]: #checks if the Server is the same as the one you want to stop
                await ctx.respond(f"The {gameRunning} is currently running!")
                return  
            
            else: #stops the Server
                serverFile = config[server]["path"]
                command = [config[server]["fileName"], action]
                process = subprocess.Popen(command, cwd=serverFile,)
                await ctx.respond(f"**{config[server]['serverName']}** is shutting down! please wait about 30 seconds until the server is fully stopped!")
                await self.bot.change_presence(status=None, activity=None)
                running = False
                gameRunning = None
                return running, gameRunning
            
        #restarts the Server
        elif action == "restart":
            if running == False:
                await ctx.respond("No Server is running!")
                return
            elif gameRunning != config[server]["serverName"]:
                await ctx.respond(f"{gameRunning} is currently running!")
                return  
            else:
                serverFile = config[server]["path"]
                command = [config[server]["fileName"], action]
                process = subprocess.Popen(command, cwd=serverFile,)
                await ctx.respond(f"**{gameRunning}** is restarting!")
                return running, gameRunning
            
        #updates the Server
        elif action == "update":
            if running:
                await ctx.respond(f"please stop the **{gameRunning}** beforehand!")
                return  
            else:
                serverFile = config[server]["path"]
                command = [config[server]["fileName"], action]
                process = subprocess.Popen(command, cwd=serverFile,)
                await ctx.respond(f"**{config[server]['serverName']}** is updating! please wait about 5 minutes until the server is fully updated!")
                return running, gameRunning



def setup(bot):
    bot.add_cog(gameservers(bot))
    
