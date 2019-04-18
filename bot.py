# -*- coding: utf-8 -*-

import os

import discord
from discord.ext import commands

import botdata as bd
from debug import cOut


class Sparks(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix=None, description=bd.conf["description"])

        if not os.path.isdir("cogs"):
            os.mkdir("cogs")

        try:
            self.run(bd.conf["token"])
        except discord.LoginFailure:
            cOut("Token invalid. Authentication failiure.")
            
            # RESET TOKEN
            bd.conf["token"] = ""
            input("Press Enter to exit.")
            raise SystemExit()

    async def on_connect(self):
        cOut("Connection established with latency: {}ms".format(int(self.latency * 1000)))

    async def on_disconnect(self):
        cOut("Client has lost connection.")

    async def on_ready(self):
        cOut("Bot is now accepting commands.\n-----")
        cOut("USERNAME: {}".format(self.user))
        cOut("ID: {}".format(self.user.id))
        cOut("Connected to {} guilds.\n-----".format(len(self.guilds)))

        self.load_all()

    async def get_prefix(self, message):
        if bd.getServer(message.guild.id) is None:
            bd.addServer(message.guild.id)

        return bd.getServer(message.guild.id)["prefix"]

    async def on_guild_join(self, guild):
        bd.addServer(guild.id)
        await guild.owner.send(embed=self.welcome(guild))

    async def on_guild_remove(self, guild):
        bd.delServer(guild.id)

    #  N O N  -  A S Y N C  #

    def load_module(self, module):
        try:
            self.load_extension("cogs.{}".format(module))
            cOut("Loaded module: {}".format(module))
            return True
        except Exception as e:
            cOut("Failed to load module {}: {}".format(module, e))
            return e

    def load_all(self):
        success, total = 0, 0

        for i in [f.replace(".py", "") for f in os.listdir("cogs") if os.path.isfile("cogs/" + f)
        ]:
            total += 1
            if self.load_module(i):
                success += 1
        cOut("Finished loading modules. ({}/{} Successful)".format(success, total))

    def welcome(self, guild):
        return discord.Embed(color=discord.Color.blue(), 
                             description=":white_check_mark: ``Thanks for adding me to your guild, '{}'!``".format(guild.name))


if __name__ == "__main__":
    print("Please start the program via launcher.py.")
    input("Press Enter to exit.")
    raise SystemExit()
