import discord
from discord.ext import commands
from util import error

import traceback
import asyncio


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")

    @commands.command(
        description="""
        *Displays information about commands that can be executed through the bot. \n``command`` parameter can be left blank to view all commands.*
        
        **Parameters**
        ``[command]`` | Command to get help about, can be left blank.

        """,
        help="{}help [command]",
    )
    async def help(self, ctx, command=None):
        async def getEmbed(cmds, page, pos, ignore_hidden=True):
            if page is None:
                embed = discord.Embed(colour=discord.Color.blurple(), title="Commands")
                embed.description = """
                
                :arrow_up: - ``Move selection up.``
                :arrow_down: - ``Move selection down.``
                :arrow_right: - ``View selected command.``
                :arrow_left: - ``Go back to selection menu.``
                """

                for cmd in cmds:
                    if not cmd.hidden or not ignore_hidden:
                        embed.add_field(name=cmd.name.capitalize(), value=cmd.brief or "No Description", inline=False)

            else:
                self.cmd = self.bot.get_command(page)
                if self.cmd is None:
                    return commands.CommandNotFound

                embed = discord.Embed(colour=discord.Color.blurple(), title="Command: {}".format(self.cmd.name.capitalize()))
                embed.description = (
                    "```{}```{}".format(self.cmd.help.format(await self.bot.get_prefix(ctx.message)), self.cmd.description)
                    or "No information provided."
                )

            return embed

        self.cmdlist = sorted(self.bot.commands, key=lambda x: x.name)

        emb = await getEmbed(self.cmdlist, command, 0)
        if emb == commands.CommandNotFound:
            raise commands.BadArgument("Command not found.")

        await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(Help(bot))
