# -*- coding: utf-8 -*-

import json
import os
import time

import discord
from aiohttp.client_exceptions import ClientConnectionError
from discord.ext import commands
import asyncio

import botdata as bd
from util import cOut, end, error, Cycle, format_number


class Sparks(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix=None, description=bd.conf["description"])

        if not os.path.isdir("cogs"):
            os.mkdir("cogs")

        try:
            print("\n-----")
            cOut("Starting bot session...")
            self.maintenance = False

            self.add_check(self.maintenance_mode)
            self.run(bd.conf["token"])

        except discord.LoginFailure as e:
            cOut("Authentication error: {}".format(e))

            # RESET TOKEN
            bd.conf["token"] = ""
            with open("config.json", "w") as f:
                json.dump(bd.conf, f, indent=4)

            raise end()

        except ClientConnectionError as e:
            cOut("Connection error: {}".format(e))
            raise end()

        except Exception as e:
            cOut("Launch error: {}".format(e))
            raise end()

    async def on_connect(self):
        cOut("Connection established with latency: {}ms".format(int(self.latency * 1000)))

    async def on_disconnect(self):
        cOut("Client has lost connection.")

    async def on_resumed(self):
        cOut("Client has regained connection.")

    async def on_ready(self):
        cOut("Bot is now accepting commands.\n-----")
        cOut("USERNAME: {}".format(self.user))
        cOut("ID: {}".format(self.user.id))
        cOut("Connected to {} guilds.\n-----".format(len(self.guilds)))

        self.load_all()
        self.startTime = time.time()

        self.loop.create_task(self.presence_changer())

    async def get_prefix(self, message):
        if bd.getServer(message.guild.id) is None:
            bd.addServer(message.guild.id)

        return bd.getServer(message.guild.id)["prefix"]

    async def on_guild_join(self, guild):
        bd.addServer(guild.id)
        await guild.owner.send(embed=self.welcome(guild))

    async def on_guild_remove(self, guild):
        bd.delServer(guild.id)

    async def maintenance_mode(self, ctx):
        return (not self.maintenance) or (await self.is_owner(ctx.author))

    #  N O N  -  A S Y N C  #

    def load_module(self, module):
        try:
            self.load_extension("cogs.{}".format(module))
            cOut("Loaded module: {}".format(module))
            return True
        except Exception as e:
            cOut("Failed to load module {}: {}".format(module, e))
            return False

    def load_all(self):
        success, total = 0, 0

        for i in [f.replace(".py", "") for f in os.listdir("cogs") if os.path.isfile("cogs/" + f)]:
            total += 1
            if self.load_module(i):
                success += 1
        cOut("Finished loading modules. ({}/{} Successful)".format(success, total))

    def welcome(self, guild):
        return discord.Embed(
            colour=discord.Colour.blue(),
            description=":white_check_mark: ``Thanks for adding me to your guild, '{}'!``".format(guild.name),
        )

    def get_total_users(self):
        count = 0
        for guild in self.guilds:
            count += len(guild.members)
        return count

    async def presence_changer(self):
        presences = Cycle(
            [
                discord.Game(name="with {} Guilds".format(format_number(len(self.guilds)))),
                discord.Activity(type=discord.ActivityType.watching, name = "{} Users".format(format_number(self.get_total_users()))),
                discord.Activity(type=discord.ActivityType.listening, name = "the $help command.")
            ]
        )

        while True:
            if self.is_ready():
                await self.change_presence(activity=presences.current)
                presences.next()
                await asyncio.sleep(10)

if __name__ == "__main__":
    print("Please start the program via launcher.py.")
    raise end()
