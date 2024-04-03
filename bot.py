import os
import time
import random
import string
import discord
from dotenv import load_dotenv
from discord.ext import tasks

from MysteryBox import MysteryBox

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
REPLAY_CHANNEL = int(os.getenv('REPLAY_CHANNEL_ID'))
LUKIE = int(os.getenv('LUKIE_ID'))
GUILD_ID = int(os.getenv('GUILD_ID'))

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

MYSTERY_BOX = MysteryBox(client)

### ON READY ###
@client.event
async def on_ready():
    replay_message.start()
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    print(f'{client.user} has connected to Discord!')


### SLASH COMMANDS ###
@tree.command(name='headphones', description='Check out my new headphones!', guild=discord.Object(id=GUILD_ID))
async def headphones(interaction):
    await interaction.response.send_message(file=discord.File('assets/headphones.jpg'))

@tree.command(name='spin', description='Spin the mystery box', guild=discord.Object(id=GUILD_ID))
async def spin(interaction):
    item = MYSTERY_BOX.spinBox()
    await interaction.response.send_message("Spinning...")
    time.sleep(.5)
    await interaction.channel.send(f'You spun a {item}!')



### ON MESSAGE ###
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif 'beter' in message.content.lower():
        await message.channel.send('Did someone say Beter? :eyes:')
    elif 'costco' in message.content.lower() or message.author.id == LUKIE:
        costco_gifs = ['https://tenor.com/view/costco-guys-costco-chicken-bake-big-justice-double-chunk-gif-18126332061581576403', 'https://tenor.com/view/costco-guys-costco-double-chunk-chocolate-cookie-double-chunk-double-chunk-chocolate-gif-11939958218838433953']
        await doReply(message, random.choice(costco_gifs))


@tasks.loop(hours=11.5)
async def replay_message():
    chance = random.randint(1, 10)
    if chance <= 5:
        channel = client.get_channel(REPLAY_CHANNEL)
        replay_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        replay_code_message = f'Someone take a look at this replay code, my teammates were so bad: {replay_code}'
        await channel.send(replay_code_message)


### Helper Functions ###
def doReply(msg, reply):
    reply_to = msg.channel.fetch_message(msg.id)
    reply_to.reply(reply)



client.run(TOKEN)