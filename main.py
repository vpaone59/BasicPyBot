"""
A basic template for a Python Discord Bot.

This is the main file that the Bot will run from.
Read through the README and make sure you have 
your .env configured before running.

To run:
'python3 main.py' or
'python main.py'
"""

import os
import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=os.getenv("PREFIX"), intents=intents)

async def main():
    """
    Runs on Bot startup
    """
    async with bot:
        # load cogs
        await load_all()  
        await bot.start(os.getenv("DISCORD_TOKEN"))
        # on_ready will run next
        
@bot.event
async def on_ready():
    """
    Runs once the bot establishes a connection with Discord
    """
    print(f'Logged in as {bot.user}')
    try:
        print("Bot ready")
    except Exception as e:
        print(f'Bot not ready\n{e}')
        
@bot.event
async def on_message(message):
    """
    Any time there is a message in any channel in any guild, this runs
    param: message - The message that was last sent to the channel
    """
    if message.author == bot.user or message.author.bot:
        # ignore messages sent from the bot itself and other bots
        # prevents infinite replying
        return
    # message_Author = message.author
    # user_message = str(message.content)

    await bot.process_commands(message) # necessary to process the Bot's message
    
@bot.command(aliases=['rf', 'rl'],description='Reloads all Cog files')
@commands.has_permissions(administrator=True)
async def refresh(ctx, extension):
    """
    Reload Cog file, same as doing unload then load.
    This allows for live development of Cogs while main.py is running.
    
    Only an admin should be able to run this
    param: ctx - The context in which the command has been executed.
    param: extension - The name of the Cog file to reload.
    """
    loaded_files=""
    if extension == 'all':
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    await bot.reload_extension(f'cogs.{filename[:-3]}')
                    loaded_files=loaded_files+"\n"+filename
                except Exception as e:
                    await ctx.send(f'```{e}\nCould not reload {filename}```')     
        await ctx.send(f'```Loaded:\n{loaded_files}```')      
    else:
        try:
            await bot.reload_extension(f'cogs.{extension}')
            await ctx.send(f'```Cog {extension}.py reloaded```')
        except commands.ExtensionNotFound as e:
            await ctx.send(f'```{e}\nCog {extension}.py not in directory```')
        except Exception as e:
            await ctx.send(f'```{e}\nCog {extension}.py could not be reloaded. Check the logs for more info.```')
    
async def load_all():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
            except Exception as e:
                print(f'{e}\nCould not load {filename}')    


asyncio.run(main())