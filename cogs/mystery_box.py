import discord
from discord import app_commands
from discord.ext import commands

from bin.MysteryBox import MysteryBox

MYSTERY_BOX = MysteryBox()
SPIN_COST = 25


class MysteryBoxCog(commands.Cog, name='MysteryBox'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # /headphones
    @app_commands.command(name='headphones', description='Check out my new headphones!')
    async def headphones(self, ctx: discord.Interaction):
        if MYSTERY_BOX.hasHeadphones(ctx.user):
            await ctx.response.send_message(
                file=discord.File('assets/headphones.jpg'),
                content='Presenting your legitimately owned headphones!',
            )
            return
        if MYSTERY_BOX.getMichaelPoints(ctx.user) >= 50:
            await ctx.response.send_message(
                file=discord.File('assets/headphones.jpg'),
                content=f'`{MYSTERY_BOX.updateMichaelPoints(ctx.user, -50)}`',
            )
        else:
            await ctx.response.send_message('You need 50 Michael Points to use this')

    # /spin
    @app_commands.checks.cooldown(1, 5)
    @app_commands.command(name='spin', description=f'Spin the mystery box for {SPIN_COST} Michael Points')
    async def spin(self, ctx: discord.Interaction):
        if MYSTERY_BOX.getMichaelPoints(ctx.user) >= SPIN_COST:
            embedded_result = MYSTERY_BOX.spinBox(ctx.user)
            await ctx.response.send_message(
                content=f'`{MYSTERY_BOX.updateMichaelPoints(ctx.user, SPIN_COST * -1)}`\n',
                embed=embedded_result,
                delete_after=120,
            )
        else:
            await ctx.response.send_message(f'You need `{SPIN_COST}` Michael Points to use this')

    # /inventory <user>
    @app_commands.checks.cooldown(1, 5)
    @app_commands.command(name='inventory', description="Display yours or another user's inventory")
    async def inventory(self, ctx: discord.Interaction, user: discord.User = None):
        if user is None:
            user = ctx.user
        await ctx.response.send_message(embed=MYSTERY_BOX.showInventory(user))

    # /sell <item>
    @app_commands.command(name='sell', description='Sell an owned item in exchange for Michael Points (case-sensitive)')
    async def sell(self, ctx: discord.Interaction, item: str):
        item_sold, sell_amount = MYSTERY_BOX.sellItem(ctx.user, item)
        if item_sold is None:
            await ctx.response.send_message(
                f'You either incorrectly typed your item or you do not own a "{item}"\n'
                '`<item>` should be case-sensitive (I.e. Sawed-Off is different from sawed-off)',
                ephemeral=True,
            )
            return
        await ctx.response.send_message(f'{ctx.user.mention} sold `{item_sold}` for `{sell_amount}` Michael Points')


async def setup(bot: commands.Bot):
    await bot.add_cog(MysteryBoxCog(bot))
