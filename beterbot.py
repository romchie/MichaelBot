import discord
import asyncio
import random
import string

# Replace 'your_token_here' with your bot's actual token
TOKEN = 'MTIxMDY5NDgyOTA1MTIxNTkxMg.GWKIeO.E8fI-Fh8hz96B-h7pSN3lbsX1LDqg8IAYXkpY8'

# Replace 'channel_id_here' with the actual channel ID you want to post in
CHANNEL_ID = 1210694638130831372

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
client.run(TOKEN)

@client.event
async def on_ready(self):
    print(f'{self.user} has connected to Discord!')
    self.channel = self.get_channel(CHANNEL_ID)
    if self.channel:
        while True:
            # Generates a random string of 5 capital letters
            replay_code = ''.join(random.choices(string.ascii_uppercase, k=5))
            message = f"hey guys check out this replay code: {replay_code}"
            await self.channel.send(message)
            # Wait for a specific period before sending the next message
            # Here, it waits for 3600 seconds (1 hour), adjust as needed
            await asyncio.sleep(5)

# async def ping(self, ctx):
#     channel = self.get_channel('1210694638130831372')

