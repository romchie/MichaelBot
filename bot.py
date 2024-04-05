import os
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
client = commands.Bot(command_prefix='/', intents=intents)
# tree = discord.app_commands.CommandTree(client)

MYSTERY_BOX = MysteryBox()
COSTCO_GIFS = ['https://tenor.com/view/costco-guys-costco-chicken-bake-big-justice-double-chunk-gif-18126332061581576403', 'https://tenor.com/view/costco-guys-costco-double-chunk-chocolate-cookie-double-chunk-double-chunk-chocolate-gif-11939958218838433953']



### ON READY ###
@client.event
async def on_ready():
    replay_message.start()
    await client.tree.sync()
    await client.get_channel(REPLAY_CHANNEL).send('i\'m alive :)')
    print(f'{client.user} has connected to Discord!')

### ON MESSAGE ###
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif 'beter' in message.content.lower():
        await message.channel.send('Did someone say Beter? :eyes:')
    elif 'costco' in message.content.lower():
        await message.reply(random.choice(COSTCO_GIFS))
    elif 'michael' in message.content.lower():
        full_str = message.content
        split_up = full_str.split()
        if split_up[-1] == 'michael':
            await message.channel.send(full_str.replace('michael', str(message.author)))


### SLASH COMMANDS ###
@client.tree.command(name='headphones', description='Check out my new headphones!')
async def headphones(interaction):
    await interaction.response.send_message(file=discord.File('assets/headphones.jpg'))

@app_commands.checks.cooldown(1, 5)
@client.tree.command(name='spin', description='Spin the mystery box')
async def spin(interaction):
    await interaction.response.send_message(MYSTERY_BOX.spinBox(interaction.user))

@app_commands.checks.cooldown(1, 5)
@client.tree.command(name='inventory', description='Display your inventory')
async def inventory(interaction):
    await interaction.response.send_message(MYSTERY_BOX.showInventory(interaction.user))

# Cooldown Errors
@spin.error
@inventory.error
async def cooldown_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(str(error), ephemeral=True)


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