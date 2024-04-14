import os
import sys
import random
import string
import asyncio
import discord
from discord import app_commands
from discord.ext import tasks
from discord.ext import commands
from dotenv import load_dotenv

from bin.MysteryBox import MysteryBox

# load env variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
MAIN_CHANNEL = int(os.getenv('MAIN_CHANNEL_ID'))
GUILD_ID = int(os.getenv('GUILD_ID'))
# specific users
ME = int(os.getenv('ROMCH_ID'))
LUKIE = int(os.getenv('LUKIE_ID'))
NATHANIEL = int(os.getenv('NATHANIEL_ID'))
ALLIE = int(os.getenv('ALLIE_ID'))

# initialize bot
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

MYSTERY_BOX = MysteryBox()
COSTCO_GIFS = ['https://tenor.com/view/costco-guys-costco-chicken-bake-big-justice-double-chunk-gif-18126332061581576403', 'https://tenor.com/view/costco-guys-costco-double-chunk-chocolate-cookie-double-chunk-double-chunk-chocolate-gif-11939958218838433953']
NATHANIEL_GIFS = ['https://tenor.com/view/nathaniel-b-gif-26365586', 'https://tenor.com/view/nathanial-b-breaking-bad-hank-breaking-bad-gd-flux-gif-26363420', 'https://tenor.com/view/nathaniel-goofy-ass-okbr-spongebob-squarepants-gif-16697139']
SPIN_COST = 25

### Client Events ###
@client.event
async def on_ready():
    if 'sync' in sys.argv:
        await tree.sync()
        # for guild in client.guilds:
        #     await tree.sync(guild=guild)
    if 'notify' in sys.argv:
        await client.get_channel(MAIN_CHANNEL).send('i\'m alive :)')

    # always do:
    michaelPointsDrop.start()
    # replayMessage.start()
    await client.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name='I\'m Michael'))
    print(f'{client.user} has connected to Discord!')
    

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    if message.author.id == NATHANIEL:
        await message.reply(content=random.choice(NATHANIEL_GIFS), delete_after=5)
    # elif message.author == LUKIE:
    #     await message.add_reaction("")
    if 'beter' in message.content.lower():
        await message.channel.send('Did someone say Beter? :eyes:')
    if 'costco' in message.content.lower():
        await message.reply(random.choice(COSTCO_GIFS))
    if 'michael' in message.content.lower():
        if message.content.lower() == 'thank you michael' or message.content.lower() == 'thanks michael':
            await message.channel.send(f'you\'re welcome {message.author}')
            return
        full_str = message.content.lower()
        split_up = full_str.split()
        if split_up[-1] == 'michael':
            try:
                if split_up[-2] == 'sorry':
                    await message.channel.send(f'it\'s okay {message.author}')
                    return
            except IndexError:
                pass
            await message.channel.send(full_str.replace('michael', str(message.author)))
    if 'hello bro' == message.content.lower():
        await message.channel.send('hello bro')
    try: # no cheating for /headphones!
        if 'headphones.' in message.content or 'headphones' in message.attachments[0].url:
            print(f'{message.author} tried cheating /headphones')
            await message.channel.send(f'Hey {message.author.mention}! No cheating for /headphones! *-25 michael points*', )
            await message.delete()
            MYSTERY_BOX.updateMichaelPoints(message.author, -25)
    except IndexError:
        pass


@client.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.User):
    # print(f'{user} reacted with a {reaction.emoji}')
    # await reaction.message.channel.send(f'{user} reacted with a {reaction.emoji}')
    return



### Might need to put this under command function defs ###
# client.tree.clear_commands(guild=ctx.guild)
# await client.tree.sync(guild=ctx.guild)

### Slash Commands ###
# /ping
@app_commands.checks.cooldown(1, 10)
@tree.command(name='ping', description='This is a test command')
async def ping(ctx: discord.Interaction):
    await ctx.response.send_message('pong!')

# /headphones
@tree.command(name='headphones', description='Check out my new headphones!')
async def headphones(ctx: discord.Interaction):
    if MYSTERY_BOX.getMichaelPoints(ctx.user) >= 50:
        await ctx.response.send_message(file=discord.File('assets/headphones.jpg'), content=f'*{MYSTERY_BOX.updateMichaelPoints(ctx.user, -50)}*')
    else:
        await ctx.response.send_message(f'You need 50 Michael Points to use this')

# /spin
@app_commands.checks.cooldown(1, 5)
@tree.command(name='spin', description=f'Spin the mystery box for {SPIN_COST} Michael Points')
async def spin(ctx: discord.Interaction):
    if MYSTERY_BOX.getMichaelPoints(ctx.user) >= SPIN_COST:
        await ctx.response.send_message(f'{MYSTERY_BOX.updateMichaelPoints(ctx.user, -SPIN_COST)}\n{MYSTERY_BOX.spinBox(ctx.user)}', delete_after=10)
    else:
        await ctx.response.send_message(f'You need {SPIN_COST} Michael Points to use this')

# /inventory <user>
@app_commands.checks.cooldown(1, 5)
@tree.command(name='inventory', description='Display yours or another user\'s inventory with /inventory <user>')
async def inventory(ctx: discord.Interaction, user: discord.User=None):
    if user == None:
        user = ctx.user
    await ctx.response.send_message(MYSTERY_BOX.showInventory(user), delete_after=60)

# /mp
@app_commands.checks.cooldown(1, 5)
@tree.command(name='mp', description='Check how many Michael Points you have')
async def mp(ctx: discord.Interaction):
    await ctx.response.send_message(f'You have {MYSTERY_BOX.getMichaelPoints(ctx.user)} Michael Points')

# /fp
@app_commands.checks.cooldown(1, 5)
@tree.command(name='fp', description='Check how many Freaky Points you have')
async def mp(ctx: discord.Interaction):
    await ctx.response.send_message(f'You have {MYSTERY_BOX.getFreakyPoints(ctx.user)} Freaky Points')

# /leaderboard
@app_commands.checks.cooldown(1, 5)
@tree.command(name='leaderboard', description='View the Michael Points Leaderboard')
async def leaderboard(ctx: discord.Interaction):
    await ctx.response.send_message(f'{MYSTERY_BOX.showLeaderboard()}')

# /applymp <user> <val>
@tree.command(name='applymp', description='Add/Deduct a user\'s Michael Points')
async def applymp(ctx: discord.Interaction, user: discord.User, val: int):
    if ctx.user.id == ME:
        MYSTERY_BOX.updateMichaelPoints(user, val)
        if val >= 0:
            await ctx.response.send_message(f'Gave {val} Michael Points to {user.mention}')
        elif val < 0:
            await ctx.response.send_message(f'Deducted {val*-1} Michael Points from {user.mention}')
    else:
        await ctx.response.send_message('You do not have access to this command', ephemeral=True)

# /applyfp <user> <val>
@tree.command(name='applyfp', description='Add/Deduct a user\'s Freaky Points')
async def applyfp(ctx: discord.Interaction, user: discord.User, val: int):
    if ctx.user.id == ME or ctx.user.id == ALLIE:
        MYSTERY_BOX.updateFreakyPoints(user, val)
        if val >= 0:
            await ctx.response.send_message(f'Gave {val} Freaky Points to {user.mention}')
        elif val < 0:
            await ctx.response.send_message(f'Deducted {val*-1} Freaky Points from {user.mention}')
    else:
        await ctx.response.send_message('You do not have access to this command', ephemeral=True)


        
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

@tasks.loop(minutes=5)
async def michaelPointsDrop():
    chance = random.randint(1, 10)
    if chance <= 5:
        channel = client.get_channel(MAIN_CHANNEL)
        num_points = random.randint(10, 50)
        notif = await channel.send(content=f'Quick! First person to react gets `{num_points}` Michael Points!')
        await notif.add_reaction('\U00002705')

        def check(reaction: discord.Reaction, user: discord.User):
            return reaction.emoji == '\U00002705' and user != client.user #and user.id != NATHANIEL
        
        try:
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
            # -- if nathaniel skill spins --
            # if user.id == 594989623877304320:
            #     await channel.send('hold up, ain\'t he nathaniel b?')
            #     MYSTERY_BOX.updateMichaelPoints(user, -num_points)
            #     await channel.send(f'{user.mention} lost {num_points} Michael Points')
            #     return
            # ------------------------------
            await channel.send(f'{user.mention} claimed `{num_points}` Michael Points!')
            MYSTERY_BOX.updateMichaelPoints(user, num_points)
        except asyncio.TimeoutError:
            await channel.send(f'Nobody reacted in time...')
    



# keep at bottom of file
client.run(TOKEN)