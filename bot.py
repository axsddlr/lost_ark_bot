import os

import discord
from discord.ext import commands
from utils.utils import cfg


def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""

    # Notice how you can use spaces in prefixes. Try to keep them simple though.
    prefixes = ["!"]

    # Check to see if we are outside of a guild. e.g DM's etc.
    if not message.guild:
        # Only allow ? to be used in DMs
        return "?"

    # allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)


def main():
    # allows privledged intents for monitoring members joining, roles editing, and role assignments
    # these need to be enabled in the developer portal as well
    intents = discord.Intents.default()

    # To enable guild intents:
    intents.guilds = True

    # To enable member intents:
    intents.members = True

    intents.messages = True

    # Set custom status to "Listening to ?help"
    activity = discord.Activity(
        type=discord.ActivityType.playing, name=f"Deathblade ;)"
    )

    bot = commands.Bot(
        command_prefix=get_prefix,
        intents=intents,
        activity=activity,
    )

    bot.remove_command("help")

    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            try:
                # This will load it
                bot.load_extension("cogs.{0}".format(filename[:-3]))
                # this is to let us know which cogs got loaded
                print("{0} is online".format(filename[:-3]))
            except:
                print("{0} was not loaded".format(filename))
                continue

    @bot.event
    async def on_ready():
        """When discord is connected"""
        print(f"{bot.user.name} has connected to Discord!")

    # Run Discord bot
    bot.run(cfg["DISCORD_TOKEN"])


# This is what we're going to use to load the cogs on startup
if __name__ == "__main__":
    main()
