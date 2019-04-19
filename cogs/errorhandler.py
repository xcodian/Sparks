import discord
from discord.ext import commands
from debug import error

import traceback
import asyncio

class ErrorHanlder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, e):
        if hasattr(ctx.command, 'on_error'):
            return

        elif isinstance(e, commands.MissingRequiredArgument):
            await ctx.send(embed=error("Missing required argument."))

        elif isinstance(e, commands.MissingPermissions):
            await ctx.send(embed=error("You don't have the permissions to do this!"))

        elif isinstance(e, commands.BotMissingPermissions):
            await ctx.send(embed=error("Insufficient bot permissions."))

        elif isinstance(e, commands.NotOwner):
            await ctx.send(embed=error("Command can be executed only by bot developers."))

        elif isinstance(e, commands.BadArgument):
            if e.args:
                msg = "Invalid argument: {0.args[0]}".format(e)
            else:
                msg = "Invalid argument."

            await ctx.send(embed=error(msg))

        elif isinstance(e, commands.CommandNotFound):
            await ctx.message.add_reaction("❔")
            await asyncio.sleep(2)
            await ctx.message.remove_reaction("❔", self.bot.user)

        else:
            await ctx.send(embed=error("An internal error has occurred! This isn't your fault, and will probably be fixed in the next update. Feel free to raise an issue on https://github.com/xxcodianxx/Sparks if this issue is persistent."))
            traceback.print_exception(type(e), e, e.__traceback__)


def setup(bot):
    bot.add_cog(ErrorHanlder(bot))
