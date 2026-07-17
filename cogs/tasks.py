from discord.ext import commands


class BotTasks(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


async def setup(bot: commands.Bot):
    await bot.add_cog(BotTasks(bot))
