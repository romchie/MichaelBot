import os
import sys
import time
import random
import string
import json
import discord
from discord.ext import tasks
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

from bin.MysteryBox import MysteryBox

# load env variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
REPLAY_CHANNEL = int(os.getenv('REPLAY_CHANNEL_ID'))
LUKIE = int(os.getenv('LUKIE_ID'))
GUILD_ID = int(os.getenv('GUILD_ID'))

# initialize bot
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

MYSTERY_BOX = MysteryBox()
COSTCO_GIFS = ['https://tenor.com/view/costco-guys-costco-chicken-bake-big-justice-double-chunk-gif-18126332061581576403', 'https://tenor.com/view/costco-guys-costco-double-chunk-chocolate-cookie-double-chunk-double-chunk-chocolate-gif-11939958218838433953']


### SLASH COMMANDS ###
@app_commands.checks.cooldown(1, 10)
@tree.command(name='ping', description='This is a test command')
async def ping(ctx: discord.Interaction):
    # client.tree.clear_commands(guild=ctx.guild)
    # await client.tree.sync(guild=ctx.guild)
    await ctx.response.send_message('pong!')

@tree.command(name='headphones', description='Check out my new headphones!')
async def headphones(ctx: discord.Interaction):
    # client.tree.clear_commands(guild=ctx.guild)
    # await client.tree.sync(guild=ctx.guild)
    await ctx.response.send_message(file=discord.File('assets/headphones.jpg'), content=f'*{MYSTERY_BOX.updateMichaelPoints(ctx.user, -5)}*')

@app_commands.checks.cooldown(1, 5)
@tree.command(name='spin', description='Spin the mystery box')
async def spin(ctx: discord.Interaction):
    # client.tree.clear_commands(guild=ctx.guild)
    # await client.tree.sync(guild=ctx.guild)
    await ctx.response.send_message(MYSTERY_BOX.spinBox(ctx.user))

@app_commands.checks.cooldown(1, 5)
@tree.command(name='inventory', description='Display your inventory')
async def inventory(ctx: discord.Interaction):
    # client.tree.clear_commands(guild=ctx.guild)
    # await client.tree.sync(guild=ctx.guild)
    await ctx.response.send_message(MYSTERY_BOX.showInventory(ctx.user))

@app_commands.checks.cooldown(1, 5)
@tree.command(name='mp', description='Check how many Michael Points you have')
async def mp(ctx: discord.Interaction):
    # client.tree.clear_commands(guild=None)
    # await client.tree.sync(guild=None)
    await ctx.response.send_message(MYSTERY_BOX.showMichaelPoints(ctx.user))


### ON READY ###
@client.event
async def on_ready():
    await tree.sync()
    # for guild in client.guilds:
    #     await tree.sync(guild=guild)

    if sys.argv[1] == 'True': # if makefile NOTIFY == 'True' (default)
        replay_message.start()
        await client.get_channel(REPLAY_CHANNEL).send('i\'m alive :)')
    print(f'{client.user} has connected to Discord!')
    

### ON MESSAGE ###
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    # elif message.content == 'test':
    #     await message.add_reaction('�')
    # elif message.author == LUKIE:
    #     await message.add_reaction("")
    if 'beter' in message.content.lower():
        await message.channel.send('Did someone say Beter? :eyes:')
    if 'costco' in message.content.lower():
        await message.reply(random.choice(COSTCO_GIFS))
    if 'michael' in message.content.lower():
        full_str = message.content.lower()
        split_up = full_str.split()
        if split_up[-1] == 'michael':
            await message.channel.send(full_str.replace('michael', str(message.author)))



### Cooldown Errors ###
@tree.error
async def cooldown_error(ctx: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        await ctx.response.send_message(f'Stop fuckin spamming! Ay I\'m Michael *(cooldown for {round(error.retry_after, 2)}s)*', ephemeral=True)

### Looped Tasks ###
@tasks.loop(hours=11.5)
async def replay_message():
    chance = random.randint(1, 10)
    if chance <= 5:
        channel = client.get_channel(REPLAY_CHANNEL)
        replay_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        replay_code_message = f'Someone take a look at this replay code, my teammates were so bad: {replay_code}'
        await channel.send(replay_code_message)



# keep at bottom of file
client.run(TOKEN)