import discord
from discord.ext import commands
import asyncio


from util import cOut, error
import util

import botdata as bd

class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # will do this later

def setup(bot):
    bot.add_cog(Settings(bot))