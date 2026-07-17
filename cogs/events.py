import random
import discord
from discord.ext import commands

from bin.MysteryBox import MysteryBox
from assets.CustomEmoji import MP_EMOJI

MYSTERY_BOX = MysteryBox()

COSTCO_GIFS = [
    'https://tenor.com/view/costco-guys-costco-chicken-bake-big-justice-double-chunk-gif-18126332061581576403',
    'https://tenor.com/view/costco-guys-costco-double-chunk-chocolate-cookie-double-chunk-double-chunk-chocolate-gif-11939958218838433953',
]
NATHANIEL_GIFS = [
    'https://tenor.com/view/nathaniel-b-gif-26365586',
    'https://tenor.com/view/nathanial-b-breaking-bad-hank-breaking-bad-gd-flux-gif-26363420',
    'https://tenor.com/view/nathaniel-goofy-ass-okbr-spongebob-squarepants-gif-16697139',
]


class Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.NATHANIEL: int = bot.NATHANIEL
        self.MUDAE_CHANNEL: int = bot.MUDAE_CHANNEL

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        if message.author.id == self.NATHANIEL and message.channel.id != self.MUDAE_CHANNEL and self.MUDAE_CHANNEL is not None:
            await message.reply(content=random.choice(NATHANIEL_GIFS), delete_after=5)
            return

        if 'beter' in message.content.lower():
            await message.channel.send('Did someone say Beter? :eyes:')

        if 'costco' in message.content.lower():
            await message.reply(random.choice(COSTCO_GIFS))

        if 'michael' in message.content.lower():
            full_str = message.content.lower()
            if full_str in ('thank you michael', 'thanks michael'):
                await message.channel.send(f'you\'re welcome {message.author}')
                return
            split_up = full_str.split()
            if split_up[-1] == 'michael':
                if len(split_up) >= 2 and split_up[-2] == 'sorry':
                    await message.channel.send(f'it\'s okay {message.author}')
                    return
                await message.channel.send(full_str.replace('michael', str(message.author)))

        if message.content.lower() == 'hello bro':
            await message.channel.send('hello bro')

        try:  # no cheating for /headphones!
            if 'headphones.' in message.content or 'headphones' in message.attachments[0].url:
                print(f'{message.author} tried cheating /headphones')
                await message.channel.send(
                    f'Hey {message.author.mention}! No cheating for /headphones! *-25 michael points*'
                )
                await message.delete()
                MYSTERY_BOX.updateMichaelPoints(message.author, -25)
        except IndexError:
            pass

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        return


async def setup(bot: commands.Bot):
    await bot.add_cog(Events(bot))
