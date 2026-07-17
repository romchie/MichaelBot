import os
import sys
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv(os.getenv('BOT_ENV', '.env.romchverse'))
load_dotenv('.env.common')
TOKEN = os.getenv('DISCORD_TOKEN')

COGS = [
    'cogs.events',
    'cogs.points',
    'cogs.mystery_box',
    'cogs.tasks',
]


class MichaelBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)

        # expose env config as bot attributes so cogs can read them
        self.MAIN_CHANNEL = int(os.getenv('MAIN_CHANNEL_ID'))
        mudae = os.getenv('MUDAE_CHANNEL_ID')
        self.MUDAE_CHANNEL = int(mudae) if mudae else None
        self.GUILD_ID = int(os.getenv('GUILD_ID'))
        self.ME = int(os.getenv('ROMCH_ID'))
        self.LUKIE = int(os.getenv('LUKIE_ID'))
        self.NATHANIEL = int(os.getenv('NATHANIEL_ID'))
        self.ALLIE = int(os.getenv('ALLIE_ID'))

    async def setup_hook(self):
        for cog in COGS:
            await self.load_extension(cog)

        if 'sync' in sys.argv:
            await self.tree.sync()

    async def on_ready(self):
        if 'notify' in sys.argv:
            await self.get_channel(self.MAIN_CHANNEL).send("i'm alive :)")

        await self.change_presence(
            status=discord.Status.online,
            activity=discord.CustomActivity(name="I'm Michael"),
        )
        print(f'{self.user} has connected to Discord!')


async def on_app_command_error(ctx: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        await ctx.response.send_message(
            f"Stop fuckin spamming! Ay I'm Michael *(cooldown for {round(error.retry_after, 2)}s)*",
            ephemeral=True,
        )


def _run(*extra_args):
    bot = MichaelBot()
    bot.tree.on_error = on_app_command_error
    bot.run(TOKEN)


def main():
    _run()


def sync():
    sys.argv.append('sync')
    _run()


def notify():
    sys.argv.append('notify')
    _run()


if __name__ == '__main__':
    _run()
