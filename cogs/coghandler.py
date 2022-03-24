from discord.commands import slash_command
from discord.ext import commands
from discord.ext.commands import has_permissions

from utils.utils import cfg

guilds = [cfg["GUILD_ID"]]


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="load", guild_ids=guilds)
    @has_permissions(manage_guild=True)
    async def load(self, ctx, *, cog: str):
        try:
            self.bot.load_extension(cog)
        except commands.ExtensionError:
            await ctx.send("**`ERROR:`**")
        else:
            await ctx.send("**`SUCCESS`**")

    @slash_command(name="unload", guild_ids=guilds)
    @has_permissions(manage_guild=True)
    async def unload(self, ctx, *, cog: str):
        print(cog)
        try:
            self.bot.unload_extension(cog)
        except commands.ExtensionError:
            await ctx.send("**`ERROR:`**")
        else:
            await ctx.send("**`SUCCESS`**")

    @slash_command(name="reload", guild_ids=guilds)
    @has_permissions(manage_guild=True)
    async def reload(self, ctx, *, cog: str):
        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except commands.ExtensionError:
            await ctx.send("**`ERROR:`**")
        else:
            await ctx.send("**`SUCCESS`**")

    @slash_command(name="shards", guild_ids=guilds)
    @has_permissions(manage_guild=True)
    async def getShards(self, ctx):
        await ctx.send("Shards: " + str(self.bot.shard_count))


def setup(bot):
    bot.add_cog(Owner(bot))
