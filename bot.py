import os
import discord
import time
import random
import string

from dotenv import load_dotenv
from discord.ext import tasks

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
REPLAY_CHANNEL = int(os.getenv('REPLAY_CHANNEL_ID'))

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    guild_count = 0
    for guild in client.guilds:
        print(f'- {guild.id} (name: {guild.name})')
        guild_count += 1
    print("Bot is in " + str(guild_count) + " guilds.")

    # initialize tasks
    replay_message.start()

@client.event
async def on_message(message):
    if message.content == 'test':
        print(message)
        await message.channel.send('test received!')
    elif 'beter' in message.content.lower() and message.author.bot == False:
        await message.channel.send('Did someone say Beter? :eyes:')

@tasks.loop(seconds=10)
async def replay_message():
    print('attempting print')
    channel = client.get_channel(REPLAY_CHANNEL)
    replay_code = ''.join(random.choices(string.ascii_uppercase, k=6))
    replay_code_message = f"Someone take a look at this replay code, my teammates were so bad - {replay_code}"
    await channel.send(replay_code_message)

client.run(TOKEN)