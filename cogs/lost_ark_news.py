import time
from configparser import ConfigParser
from datetime import datetime

import discord
import requests
import tzlocal
import ujson as json
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dhooks import Webhook, Embed, File
from discord.commands import slash_command
from discord.ext import commands

from utils.utils import lost_ark_exists, crimson, headers, cfg

config = ConfigParser()
config.read('webhooks.cfg')

guilds = [cfg["GUILD_ID"]]
lost_ark_wh = config.get('webhooks', 'LOST_ARK_WEBHOOK')


def getLostArkUpdates():
    url = 'https://lost-ark-api.vercel.app/news/updates'
    vercel = requests.get(url)
    if vercel.status_code == 200:
        return vercel.json()
    else:
        return None


def getserver(world):
    url = f"https://lost-ark-api.vercel.app/server/{world}"
    vercel = requests.get(url, headers=headers)
    if vercel.status_code == 200:
        return vercel.json()
    else:
        return None


def updater(d, inval, outval):
    for k, v in d.items():
        if isinstance(v, dict):
            updater(d[k], inval, outval)
        else:
            if v == "":
                d[k] = None
    return d


class LostA_Patch(commands.Cog, name="Lost Ark Patch Notes"):
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler(timezone=str(tzlocal.get_localzone()),
                                          job_defaults={"misfire_grace_time": 800})

    async def losta_patch_monitor(self):
        await self.bot.wait_until_ready()

        saved_json = "losta_old.json"

        # call API
        responseJSON = getLostArkUpdates()

        title = responseJSON["data"][0]["title"]
        description = responseJSON["data"][0]["description"]
        thumbnail = responseJSON["data"][0]["thumbnail"]
        url = responseJSON["data"][0]["url"]

        # check if file exists
        lost_ark_exists(saved_json)

        time.sleep(5)
        # open saved_json and check title string
        f = open(
            saved_json,
        )
        data = json.load(f)
        res = updater(data, "", None)
        check_file_json = res["data"][0]["title"]

        # compare title string from file to title string from api then overwrite file
        if check_file_json == title:
            return
        elif check_file_json != title:

            hook = Webhook(lost_ark_wh)

            embed = Embed(
                title="Lost Ark",
                description=f"[{title}]({url})\n\n{description}",
                color=crimson,
                timestamp="now",  # sets the timestamp to current time
            )
            embed.set_footer(text="Lost Ark Bot")
            embed.set_image(url=thumbnail)
            file = File("./assets/images/LA_logo.png", name="LA_logo.png")
            embed.set_thumbnail(url="attachment://LA_logo.png")

            hook.send(embed=embed, file=file)

            f = open(saved_json, "w")
            print(json.dumps(responseJSON), file=f)

        f.close()

    @slash_command(
        name="server",
        guild_ids=guilds,
    )
    async def lastatus(self, ctx, world_name):
        responseJSON = getserver(world_name)

        status = responseJSON["status"]

        if status != 200:
            print("error parsing stream")
        elif status == 200:
            base = responseJSON["data"][f"{world_name}"]

            # Get current time
            now = datetime.now()

            embed = discord.Embed(
                title=f"{world_name}\n\n",
                description=f"\n\n\n**__Status__**\n{base}",
                colour=crimson,
                timestamp=now,
            )
            embed.set_footer(text="Lost Ark bot")
            file = discord.File(
                "./assets/images/LA_logo.png", filename="LA_logo.png"
            )
            embed.set_thumbnail(url="attachment://LA_logo.png")

            await ctx.respond(file=file, embed=embed)
        else:
            print("result fail")

    @commands.Cog.listener()
    async def on_ready(self):

        scheduler = self.scheduler

        # add job for scheduler
        scheduler.add_job(self.losta_patch_monitor, "interval", minutes=15)

        # starting the scheduler
        scheduler.start()


def setup(bot):
    bot.add_cog(LostA_Patch(bot))
