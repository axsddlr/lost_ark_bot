import discord
from discord.commands import slash_command
from discord.ext import commands

from utils.utils import cfg

guilds = [cfg["GUILD_ID"]]


class Ping(commands.Cog, name="Ping"):
    """Receives ping commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(name="ping", description='Check bot latency.', guild_ids=guilds)
    async def ping(self, ctx):
        embed = discord.Embed(
            title='🏓|Pong!',
            description=f'Latency: {self.bot.latency} ms',
            color=discord.Color.green()
        )
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Ping(bot))
