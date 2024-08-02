import os
import sys
import random
import string
import asyncio
import discord
from discord import app_commands
from discord import interactions
from discord.ext import tasks
from dotenv import load_dotenv
import paginator

from bin.MysteryBox import MysteryBox
from assets.CustomEmoji import *

# load env variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
MAIN_CHANNEL = int(os.getenv('MAIN_CHANNEL_ID'))
MUDAE_CHANNEL = int(os.getenv('MUDAE_CHANNEL_ID'))
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


class MPointDropView(discord.ui.View):
    message: discord.Message = None
    mpoints: int = None

    async def on_timeout(self) -> None:
        await self.message.channel.send('Nobody reacted in time...')

    @discord.ui.button(emoji='\U00002705', style=discord.ButtonStyle.secondary)
    async def checkmark(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            self.stop()
            MYSTERY_BOX.updateMichaelPoints(interaction.user, self.mpoints)
            await interaction.channel.send(f'**{interaction.user.name}** claimed **{self.mpoints}**{MP_EMOJI}')
            await interaction.response.defer()
        except:
            pass


class PaginationView(discord.ui.View):
    current_page : int = 1
    sep : int = 5

    async def send(self, ctx):
        self.message = await ctx.send(view=self)
        await self.update_message(self.data[:self.sep])

    def create_embed(self, data):
        embed = discord.Embed(title=f"User List Page {self.current_page} / {int(len(self.data) / self.sep) + 1}")
        for item in data:
            embed.add_field(name=item['label'], value=item[''], inline=False)
        return embed

    async def update_message(self,data):
        self.update_buttons()
        await self.message.edit(embed=self.create_embed(data), view=self)

    def update_buttons(self):
        if self.current_page == 1:
            self.first_page_button.disabled = True
            self.prev_button.disabled = True
            self.first_page_button.style = discord.ButtonStyle.gray
            self.prev_button.style = discord.ButtonStyle.gray
        else:
            self.first_page_button.disabled = False
            self.prev_button.disabled = False
            self.first_page_button.style = discord.ButtonStyle.green
            self.prev_button.style = discord.ButtonStyle.primary

        if self.current_page == int(len(self.data) / self.sep) + 1:
            self.next_button.disabled = True
            self.last_page_button.disabled = True
            self.last_page_button.style = discord.ButtonStyle.gray
            self.next_button.style = discord.ButtonStyle.gray
        else:
            self.next_button.disabled = False
            self.last_page_button.disabled = False
            self.last_page_button.style = discord.ButtonStyle.green
            self.next_button.style = discord.ButtonStyle.primary

    def get_current_page_data(self):
        until_item = self.current_page * self.sep
        from_item = until_item - self.sep
        if not self.current_page == 1:
            from_item = 0
            until_item = self.sep
        if self.current_page == int(len(self.data) / self.sep) + 1:
            from_item = self.current_page * self.sep - self.sep
            until_item = len(self.data)
        return self.data[from_item:until_item]


    @discord.ui.button(label="|<",
                       style=discord.ButtonStyle.green)
    async def first_page_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page = 1

        await self.update_message(self.get_current_page_data())

    @discord.ui.button(label="<",
                       style=discord.ButtonStyle.primary)
    async def prev_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page -= 1
        await self.update_message(self.get_current_page_data())

    @discord.ui.button(label=">",
                       style=discord.ButtonStyle.primary)
    async def next_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page += 1
        await self.update_message(self.get_current_page_data())

    @discord.ui.button(label=">|",
                       style=discord.ButtonStyle.green)
    async def last_page_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page = int(len(self.data) / self.sep) + 1
        await self.update_message(self.get_current_page_data())




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
    # michaelPointsDrop.start()
    # replayMessage.start()
    await client.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name='I\'m Michael'))
    print(f'{client.user} has connected to Discord!')
    

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    if message.content == 'test':
        e = discord.Embed(color=10181046)
        e.set_image(url='https://static.wikia.nocookie.net/micheals-zombies-roblox/images/f/f3/Michael.png/revision/latest?cb=20220705141814')
        # e.set_footer(text='Footer', icon_url='https://static.wikia.nocookie.net/micheals-zombies-roblox/images/f/f3/Michael.png/revision/latest?cb=20220705141814')
        e.add_field(name='Michael', value='10 MP', inline=True)
        view = discord.ui.View()
        item = discord.ui.Button(style=discord.ButtonStyle.gray, label='erm button', emoji='\U00002705')
        view.add_item(item=item)
        new_msg = await message.channel.send(embed=e, view=view) # add view=view
        # await new_msg.add_reaction('\U00002705')
    if message.content == 'test2':
        button = interactions.Button(style=interactions.ButtonStyle.PRIMARY, label="Click me!", custom_id="click_me")


    if message.author.id == NATHANIEL and message.channel.id != MUDAE_CHANNEL:
        return
        await message.reply(content=random.choice(NATHANIEL_GIFS), delete_after=5)
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

@client.event
async def on_button_click(ctx: discord.Interaction):
    print('here')
    print(ctx.data.items())


### Might need to put this under command function defs ###
# client.tree.clear_commands(guild=ctx.guild)
# await client.tree.sync(guild=ctx.guild)

### Slash Commands ###
# # /ping
# @app_commands.checks.cooldown(1, 10)
# @tree.command(name='ping', description='This is a test command')
# async def ping(ctx: discord.Interaction):
#     await ctx.response.send_message('pong!')

# /headphones
@tree.command(name='headphones', description='Check out my new headphones!')
async def headphones(ctx: discord.Interaction):
    if MYSTERY_BOX.hasHeadphones(ctx.user):
        await ctx.response.send_message(file=discord.File('assets/headphones.jpg'), content='Presenting your legitimately owned headphones!')
        return
    if MYSTERY_BOX.getMichaelPoints(ctx.user) >= 50:
        await ctx.response.send_message(file=discord.File('assets/headphones.jpg'), content=f'`{MYSTERY_BOX.updateMichaelPoints(ctx.user, -50)}`')
    else:
        await ctx.response.send_message(f'You need 50 Michael Points to use this')

# /spin
@app_commands.checks.cooldown(1, 5)
@tree.command(name='spin', description=f'Spin the mystery box for {SPIN_COST} Michael Points')
async def spin(ctx: discord.Interaction):
    if MYSTERY_BOX.getMichaelPoints(ctx.user) >= SPIN_COST:
        embedded_result = MYSTERY_BOX.spinBox(ctx.user)
        await ctx.response.send_message(content=f'`{MYSTERY_BOX.updateMichaelPoints(ctx.user, SPIN_COST*-1)}`\n', embed=embedded_result, delete_after=120)
    else:
        await ctx.response.send_message(f'You need `{SPIN_COST}` Michael Points to use this')

# /inventory <user>
@app_commands.checks.cooldown(1, 5)
@tree.command(name='inventory', description='Display yours or another user\'s inventory with /inventory <user>')
async def inventory(ctx: discord.Interaction, user: discord.User=None):
    if user == None:
        user = ctx.user
    await ctx.response.send_message(MYSTERY_BOX.showInventory(user))

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
    embeds = [discord.Embed(title="First embed"),
          discord.Embed(title="Second embed"),
          discord.Embed(title="Third embed")]
    await paginator.Simple().start(ctx, pages=embeds)
    # await ctx.response.defer()

    # leaderboard_embed = MYSTERY_BOX.showLeaderboard('mpoints')
    # await ctx.response.send_message(content='', embed=leaderboard_embed)

# /freakyboard
@app_commands.checks.cooldown(1, 5)
@tree.command(name='freakyboard', description='View the Freaky Points Leaderboard')
async def freakyboard(ctx: discord.Interaction):
    leaderboard_str = MYSTERY_BOX.showLeaderboard('fpoints')
    await ctx.response.send_message(leaderboard_str)

# /applymp <user> <val>
@tree.command(name='applymp', description='Add/Deduct a user\'s Michael Points')
async def applymp(ctx: discord.Interaction, user: discord.User, val: int):
    if ctx.user.id == ME:
        MYSTERY_BOX.updateMichaelPoints(user, val)
        if val >= 0:
            await ctx.response.send_message(f'Gave {val} Michael Points to {user.mention}')
        elif val < 0:
            await ctx.response.send_message(f'Deducted {val * -1} Michael Points from {user.mention}')
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
            await ctx.response.send_message(f'Deducted {val * -1} Freaky Points from {user.mention}')
    else:
        await ctx.response.send_message('You do not have access to this command', ephemeral=True)

# /sell <item>
@tree.command(name='sell', description='Sell an owned item in exchange for Michael Points (case-sensitive)')
async def sell(ctx: discord.Interaction, item: str):
    item_sold, sell_amount = MYSTERY_BOX.sellItem(ctx.user, item)
    if item_sold == None:
        await ctx.response.send_message(f'You either incorrectly typed your item or you do not own a "{item}"\n`<item>` should be case-sensitive (I.e. Sawed-Off is different from sawed-off)', ephemeral=True)
    await ctx.response.send_message(f'{ctx.user.mention} sold `{item_sold}` for `{sell_amount}` Michael Points')

        
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
        view = MPointDropView(timeout=60)
        view.mpoints = num_points
        notif = await channel.send(content=f'Quick! First person to react gets **{num_points}**{MP_EMOJI}!', view=view)
        view.message = notif
        await view.wait()


        # await notif.add_reaction('\U00002705')

        # def check(reaction: discord.Reaction, user: discord.User):
        #     return reaction.emoji == '\U00002705' and reaction.message == notif and user != client.user #and user.id != NATHANIEL
        
        # try:
        #     reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
        #     await channel.send(f'{user.mention} claimed `{num_points}` Michael Points!')
        #     MYSTERY_BOX.updateMichaelPoints(user, num_points)
        # except asyncio.TimeoutError:
        #     await channel.send(f'Nobody reacted in time...')
    



# keep at bottom of file
client.run(TOKEN)