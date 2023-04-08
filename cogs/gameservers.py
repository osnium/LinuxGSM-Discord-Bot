import discord
from discord.ext import commands
from discord.commands import slash_command
from discord.commands import SlashCommandGroup
from discord import Option
import subprocess
import json
import aiosqlite




cmds = ["start", "stop", "restart", "update"]


class gameservers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.running = False
        self.gameRunning = None
        self.cmds = cmds


    @commands.Cog.listener()
    async def on_ready(self):
        async with aiosqlite.connect("gameservers.db") as db:
            await db.execute("CREATE TABLE IF NOT EXISTS gameservers (serverNick TEXT PRIMARY KEY, serverName TEXT, serverPath TEXT, serverFile TEXT)")
            await db.commit()

    
    #get the Gameservers from the config file
    async def get_servers(ctx: discord.AutocompleteContext):
        async with aiosqlite.connect("gameservers.db") as db:
            gameservers = await db.execute("SELECT serverNick FROM gameservers")
            return [row[0] for row in await gameservers.fetchall()]
        

    #get the actions from the cmds list
    async def get_cmds(ctx: discord.AutocompleteContext):
        return cmds
    

    #Add a Gameserver to the Database
    @slash_command(name = "addserver", description = "Adds a Gameserver to the Database")
    async def addserver(self, ctx, servernick: Option(str), servername: Option(str), serverpath: Option(str), serverfile: Option(str)):
        if await self.bot.is_owner(ctx.author) == False:
            await ctx.respond("You are not allowed to use this command!")
            return
        async with aiosqlite.connect("gameservers.db") as db:
            doesExist = await db.execute("SELECT * FROM gameservers WHERE serverNick = ?", (servernick,))
            if bool(await doesExist.fetchall()) != False:
                await ctx.respond(f"The server {servernick} already exists!")
                return
            await db.execute("INSERT INTO gameservers VALUES (?, ?, ?, ?)", (servernick, servername, serverpath, serverfile))
            await db.commit()
            await ctx.respond(f"Added {servernick} to the Database!")
    
    #Remove a Gameserver from the Database
    @slash_command(name = "removeserver", description = "Removes a Gameserver from the Database")
    async def removeserver(self, ctx, servernick: Option(autocomplete=get_servers)):
        if await self.bot.is_owner(ctx.author) == False:
            await ctx.respond("You are not allowed to use this command!")
            return
        if self.gameRunning == servernick:
            await ctx.respond(f"{servernick} is currently running! Please stop it first!")
            return
        async with aiosqlite.connect("gameservers.db") as db:
            doesExist = await db.execute("SELECT * FROM gameservers WHERE serverNick = ?", (servernick,))
            if await doesExist.fetchall() == None:
                await ctx.respond(f"The server {servernick} does not exist!")
                return
            await db.execute("DELETE FROM gameservers WHERE serverNick = ?", (servernick,))
            await db.commit()
            await ctx.respond(f"Removed {servernick} from the Database!")

    #Starts, Stops, Restarts or Updates a Gameserver
    @slash_command(name = "server", description = "Starts, Stops, Restarts or Updates a Gameserver")
    async def server(self, ctx, server: Option(str, autocomplete=get_servers), action: Option(str, autocomplete=get_cmds)):
        gameservers = await self.get_servers()

        #Checks if the Server exists
        if server not in gameservers:
            await ctx.respond(f"The server {server} does not exist!, available servers are: {', '.join(gameservers)}")
            return
        
        #Checks if the action exists
        if action not in self.cmds:
            await ctx.respond(f"The action {action} does not exist!, available actions are: {', '.join(cmds)}")
            return

        #Starts the Server
        if action == "start":
            if self.running == True: #Checks if a Server is already running
                await ctx.respond(f"{self.gameRunning} is already running! Please stop it first!")
                return
            else: #Starts the Server
                async with aiosqlite.connect("gameservers.db") as db:
                    serverData = await db.execute("SELECT * FROM gameservers WHERE serverNick = ?", (server,))
                    serverData = await serverData.fetchall()
                    serverFile = serverData[0][2]
                    command = [serverData[0][3], action]
                    process = subprocess.Popen(command, cwd=serverFile,)
                    await ctx.respond(f"**{serverData[0][1]}** is starting!")
                    await self.bot.change_presence(status=None, activity=discord.Game(serverData[0][1]))
                    self.running = True
                    self.gameRunning = True
                    return self.running, self.gameRunning

            
        #stops the Server

        elif action == "stop":
            async with aiosqlite.connect("gameservers.db") as db:
                serverName = await db.execute("SELECT serverName FROM gameservers WHERE serverNick = ?", (server,))
            if self.running == False: #checks if a Server is running
                await ctx.respond("No Server is running!")
                return
            
            elif self.gameRunning != serverName: #checks if the Server is running
                await ctx.respond(f"The {self.gameRunning} is currently running!")
                return  
            else: #stops the Server
                async with aiosqlite.connect("gameservers.db") as db:
                    serverData = await db.execute("SELECT * FROM gameservers WHERE serverNick = ?", (server,))
                    serverData = await serverData.fetchall()
                    serverFile = serverData[0][2]
                    command = [serverData[0][3], action]
                    process = subprocess.Popen(command, cwd=serverFile,)
                    await ctx.respond(f"**{serverData[0][1]}** is shutting down! please wait about 30 seconds until the server is fully stopped!")
                    await self.bot.change_presence(status=None, activity=None)
                    self.running = False
                    self.gameRunning = None
                    return self.running, self.gameRunning
                        
        #restarts the Server
        elif action == "restart":
            async with aiosqlite.connect("gameservers.db") as db:
                serverName = await db.execute("SELECT serverName FROM gameservers WHERE serverNick = ?", (server,))

            if self.running == False:
                await ctx.respond("No Server is running!")
                return
            elif self.gameRunning != serverName:
                await ctx.respond(f"{self.gameRunning} is currently running!")
                return  
            else:
                async with aiosqlite.connect("gameservers.db") as db:
                    serverData = await db.execute("SELECT * FROM gameservers WHERE serverNick = ?", (server,))
                    serverData = await serverData.fetchall()
                    serverFile = serverData[0][2]
                    command = [serverData[0][3], action]
                    process = subprocess.Popen(command, cwd=serverFile,)
                    await ctx.respond(f"**{serverData[0][1]}** is restarting!")
                    return self.running, self.gameRunning
                
            
        #updates the Server

        elif action == "update":
            if self.running:
                await ctx.respond(f"please stop the **{self.gameRunning}** beforehand!")
                return  
            else:
                async with aiosqlite.connect("gameservers.db") as db:
                    serverData = await db.execute("SELECT * FROM gameservers WHERE serverNick = ?", (server,))
                    serverData = await serverData.fetchall()
                    serverFile = serverData[0][2]
                    command = [serverData[0][3], action]
                    process = subprocess.Popen(command, cwd=serverFile,)
                    await ctx.respond(f"**{serverData[0][1]}** is updating! please wait about 5 minutes until the server is fully updated!")
                    return self.running, self.gameRunning



    #Test Command
    @slash_command(name = "test", description = "Test Command")
    async def test(self, ctx, servername: Option(str, autocomplete=get_servers)):
        #retrieve the data from the database
        print(f"Servername: {servername}")
        async with aiosqlite.connect("gameservers.db") as db:
            serverData = await db.execute("SELECT * FROM gameservers WHERE serverNick = ?", (servername,))
            serverData = await serverData.fetchall()
            serverFile = serverData[0][2]
            command = [serverData[0][3], "start"]
            subprocess.Popen(command, cwd=serverFile,)
            await ctx.respond(f"Data0{serverData[0][0]}, Data1{serverData[0][1]}, Data2{serverData[0][2]}, Data3{serverData[0][3]}")
            await ctx.send(f"ServerFile: {serverFile}, Command: {command}")
            print(f"Type of ServerFile: {type(serverData[0][2])}")

def setup(bot):
    bot.add_cog(gameservers(bot))
    
