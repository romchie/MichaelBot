import random
import discord
from discord import app_commands
from discord.ext import commands, tasks

import paginator
from bin.MysteryBox import MysteryBox
from assets.CustomEmoji import MP_EMOJI

MYSTERY_BOX = MysteryBox()


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
        except Exception:
            pass


class Points(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ME: int = bot.ME
        self.ALLIE: int = bot.ALLIE
        self.MAIN_CHANNEL: int = bot.MAIN_CHANNEL
        self.michaelPointsDrop.start()

    def cog_unload(self):
        self.michaelPointsDrop.cancel()

    # /mp
    @app_commands.checks.cooldown(1, 5)
    @app_commands.command(name='mp', description='Check how many Michael Points you have')
    async def mp(self, ctx: discord.Interaction):
        await ctx.response.send_message(f'You have {MYSTERY_BOX.getMichaelPoints(ctx.user)} Michael Points')

    # /fp
    @app_commands.checks.cooldown(1, 5)
    @app_commands.command(name='fp', description='Check how many Freaky Points you have')
    async def fp(self, ctx: discord.Interaction):
        await ctx.response.send_message(f'You have {MYSTERY_BOX.getFreakyPoints(ctx.user)} Freaky Points')

    # /applymp <user> <val>
    @app_commands.command(name='applymp', description="Add/Deduct a user's Michael Points")
    async def applymp(self, ctx: discord.Interaction, user: discord.User, val: int):
        if ctx.user.id != self.ME:
            await ctx.response.send_message('You do not have access to this command', ephemeral=True)
            return
        MYSTERY_BOX.updateMichaelPoints(user, val)
        if val >= 0:
            await ctx.response.send_message(f'Gave {val} Michael Points to {user.mention}')
        else:
            await ctx.response.send_message(f'Deducted {val * -1} Michael Points from {user.mention}')

    # /applyfp <user> <val>
    @app_commands.command(name='applyfp', description="Add/Deduct a user's Freaky Points")
    async def applyfp(self, ctx: discord.Interaction, user: discord.User, val: int):
        if ctx.user.id not in (self.ME, self.ALLIE):
            await ctx.response.send_message('You do not have access to this command', ephemeral=True)
            return
        MYSTERY_BOX.updateFreakyPoints(user, val)
        if val >= 0:
            await ctx.response.send_message(f'Gave {val} Freaky Points to {user.mention}')
        else:
            await ctx.response.send_message(f'Deducted {val * -1} Freaky Points from {user.mention}')

    # /leaderboard
    @app_commands.checks.cooldown(1, 5)
    @app_commands.command(name='leaderboard', description='View the Michael Points Leaderboard')
    async def leaderboard(self, ctx: discord.Interaction):
        embeds = [
            discord.Embed(title='First embed'),
            discord.Embed(title='Second embed'),
            discord.Embed(title='Third embed'),
        ]
        await paginator.Simple().start(ctx, pages=embeds)

    # /freakyboard
    @app_commands.checks.cooldown(1, 5)
    @app_commands.command(name='freakyboard', description='View the Freaky Points Leaderboard')
    async def freakyboard(self, ctx: discord.Interaction):
        leaderboard_embed = MYSTERY_BOX.showLeaderboard('fpoints')
        await ctx.response.send_message(content='', embed=leaderboard_embed)

    @tasks.loop(minutes=5)
    async def michaelPointsDrop(self):
        chance = random.randint(1, 10)
        if chance <= 5:
            channel = self.bot.get_channel(self.MAIN_CHANNEL)
            num_points = random.randint(10, 50)
            view = MPointDropView(timeout=60)
            view.mpoints = num_points
            notif = await channel.send(
                content=f'Quick! First person to react gets **{num_points}**{MP_EMOJI}!', view=view
            )
            view.message = notif
            await view.wait()

    @michaelPointsDrop.before_loop
    async def before_drop(self):
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot):
    await bot.add_cog(Points(bot))
