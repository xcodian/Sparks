import discord
from discord.ext import commands
from util import error, flagParse

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
        ``-showhidden`` | Flag that shows all of the bot commands, even hidden ones.

        """,
        usage = "[command]  [-showhidden]",
        brief = "View help for bot commands."
    )
    async def help(self, ctx, *, args = None):
        def getEmbed(cmds, page, pos, ignore_hidden=True):
            if page is None:
                embed = discord.Embed(colour=discord.Color.blurple(), title="Commands")
                embed.description = """``Use the arrows to navigate the commands.``"""

                for cmd in cmds:
                    if not cmd.hidden or not ignore_hidden:
                        embed.add_field(name=cmd.name.capitalize(), value=cmd.brief or "No Description", inline=False)

                embed.set_field_at(pos, name="[**{}**]".format(embed.fields[pos].name), value=embed.fields[pos].value, inline=embed.fields[pos].inline)

            else:
                cmd = self.bot.get_command(page)
                if cmd is None:
                    return commands.CommandNotFound

                usage = cmd.usage if cmd.usage else ""

                embed = discord.Embed(colour=discord.Color.blurple())
                embed.title = "```{}{} {}```".format(ctx.prefix, cmd.name, usage)
                embed.description = cmd.description or cmd.brief or "No description"
                embed.set_author(name = "Command: {}".format(cmd.name.capitalize()))

            return embed

        self.cmdlist = sorted(self.bot.commands, key=lambda x: x.name)

        def checkflags(args):
            ignorehidden = True
            if args:
                if args.startswith("-"):
                    flags = flagParse(args, {"-showhidden": 0})

                    if flags == commands.BadArgument:
                        raise commands.BadArgument()

                    if flags == commands.MissingRequiredArgument:
                        raise commands.MissingRequiredArgument()

                    if "-showhidden" in flags.keys():
                        ignorehidden = False
                        args = None

            return getEmbed(self.cmdlist, args, 0, ignorehidden), ignorehidden


        curpage = args
        curpos = 0
        emb, ighidden= checkflags(args)

        if emb == commands.CommandNotFound:
            raise commands.BadArgument("Command not found.")

        msg = await ctx.send(embed=emb)

        navpanel = list('◀🔽🔼▶')
        for i in navpanel:
            await msg.add_reaction(i)

        while True:
            def check(reaction, user):
                return reaction.emoji in navpanel and user == ctx.author and reaction.message.id == msg.id
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)
                await msg.remove_reaction(reaction, user)
            except asyncio.TimeoutError:
                break

            if reaction.emoji == navpanel[0]:
                if not curpage is None:
                    curpage = None
                    await msg.edit(embed = getEmbed(self.cmdlist, curpage, curpos, ighidden))

            if reaction.emoji == navpanel[3]:
                if curpage is None:
                    curpage = msg.embeds[0].fields[curpos].name.lower().lstrip("[**").rstrip("**]")
                    await msg.edit(embed=getEmbed(self.cmdlist, curpage, curpos, ighidden))

            if reaction.emoji == navpanel[2]:
                if curpos > 0:
                    curpos-=1
                    await msg.edit(embed=getEmbed(self.cmdlist, curpage, curpos, ighidden))

            if reaction.emoji == navpanel[1]:
                if curpos+1 < len(msg.embeds[0].fields):
                    curpos += 1
                    await msg.edit(embed=getEmbed(self.cmdlist, curpage, curpos, ighidden))

        await msg.clear_reactions()

def setup(bot):
    bot.add_cog(Help(bot))
