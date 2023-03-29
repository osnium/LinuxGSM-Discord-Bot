import discord


intents = discord.Intents.default()
intents.members = True


bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(status=None, activity=None)
    print(f"{bot.user} is ready and online!")

bot.load_extension("cogs.gameservers")

# reload_extension is currently somewhat broken in Pycord wouldn't recommend using it

# @bot.slash_command(name="reload", description="Reloads the Gameserver Cog")
# @commands.is_owner()
# async def reload(ctx):
#     try:
#         bot.reload_extension("cogs.gameservers")
#     except Exception as e:
#         await ctx.respond(f"Error while reloading Gameserver Cog: {e}",ephemeral=True)
#     else:
#         await ctx.respond("Reloaded Gameserver Cog",ephemeral=True)



bot.run("") # run the bot with the token
