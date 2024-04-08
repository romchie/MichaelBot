import os
import sys
import time
import random
import string
import json
import asyncio
import discord
from discord.ext import tasks
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

from bin.MysteryBox import MysteryBox

# load env variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
MAIN_CHANNEL = int(os.getenv('MAIN_CHANNEL_ID'))
LUKIE = int(os.getenv('LUKIE_ID'))
GUILD_ID = int(os.getenv('GUILD_ID'))

# initialize bot
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

MYSTERY_BOX = MysteryBox()
COSTCO_GIFS = ['https://tenor.com/view/costco-guys-costco-chicken-bake-big-justice-double-chunk-gif-18126332061581576403', 'https://tenor.com/view/costco-guys-costco-double-chunk-chocolate-cookie-double-chunk-double-chunk-chocolate-gif-11939958218838433953']


### Client Events ###
@client.event
async def on_ready():
    await tree.sync()
    # for guild in client.guilds:
    #     await tree.sync(guild=guild)

    if sys.argv[1] == 'True': # if makefile NOTIFY == 'True' (default)
        # replayMessage.start()
        michaelPointsDrop.start()
        await client.get_channel(MAIN_CHANNEL).send('i\'m alive :)')
    print(f'{client.user} has connected to Discord!')
    

@client.event
async def on_message(message: discord.Message):
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

@client.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.User):
    # print(f'{user} reacted with a {reaction.emoji}')
    # await reaction.message.channel.send(f'{user} reacted with a {reaction.emoji}')
    return



### Slash Commands ###
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
    if MYSTERY_BOX.getMichaelPoints(ctx.user) >= 50:
        await ctx.response.send_message(file=discord.File('assets/headphones.jpg'), content=f'*{MYSTERY_BOX.updateMichaelPoints(ctx.user, -50)}*')
    else:
        await ctx.response.send_message(f'You need 50 Michael Points to use this')

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
    await ctx.response.send_message(f'You have {MYSTERY_BOX.getMichaelPoints(ctx.user)} Michael Points')


        
### Cooldown Errors ###
@tree.error
async def cooldown_error(ctx: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        await ctx.response.send_message(f'Stop fuckin spamming! Ay I\'m Michael *(cooldown for {round(error.retry_after, 2)}s)*', ephemeral=True)


### Looped Tasks ###
@tasks.loop(hours=11.5)
async def replayMessage():
    chance = random.randint(1, 10)
    if chance <= 5:
        channel = client.get_channel(MAIN_CHANNEL)
        replay_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        replay_code_message = f'Someone take a look at this replay code, my teammates were so bad: {replay_code}'
        await channel.send(replay_code_message)

@tasks.loop(minutes=20)
async def michaelPointsDrop():
    chance = random.randint(1, 10)
    if chance <= 5:
        channel = client.get_channel(MAIN_CHANNEL)
        msg = await channel.send(content=f'Quick! First person to react gets 10 michael points! *(60 seconds!)*')
        await msg.add_reaction('\U00002705')

        def check(reaction, user):
            return reaction.emoji == '\U00002705' and user != client.user
        try:
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
            await channel.send(f'{user} claimed 10 michael points!')
            MYSTERY_BOX.updateMichaelPoints(user, 10)
        except asyncio.TimeoutError:
            await channel.send(f'Nobody reacted in time...')



# keep at bottom of file
client.run(TOKEN)