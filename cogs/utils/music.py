# -*- coding: utf-8 -*-

import asyncio

import discord
from youtube_dl import YoutubeDL

__all__ = ["Player", "Source"]

ytdlopts = {
    "format": "bestaudio/best",
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0",
}

ffmpegopts = {"options": "-vn", "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"}

ytdl = YoutubeDL(ytdlopts)

if not discord.opus.is_loaded():
    discord.opus.load_opus("opus")


class Player:
    def __init__(self, ctx):
        self.bot = ctx.bot
        self.cog = ctx.cog

        self.guild = ctx.guild
        self.channel = ctx.channel

        self.next = asyncio.Event()
        self.songs = asyncio.Queue()

        self.entry = None
        self.volume = 0.5
        self.task = ctx.bot.loop.create_task(self.loop())

    async def kill(self):
        await self.guild.voice_client.disconnect()
        del self.cog.players[str(self.guild.id)]
        self.task.cancel()

    async def get(self):
        source = await self.songs.get()
        source.volume = self.volume
        return source

    async def play(self):
        self.guild.voice_client.play(self.entry, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
        await self.channel.send(":musical_note: Now playing: `{}`".format(self.entry))

    async def loop(self):
        while not self.bot.is_closed():
            self.next.clear()
            self.entry = await self.get()

            await self.play()
            await self.next.wait()

            if len(self.songs) < 1:
                await self.kill()


class Source(discord.PCMVolumeTransformer):
    def __init__(self, source, volume=0.5, **kwargs):
        super().__init__(source, volume)
        self.data = kwargs.get("data")

    def __str__(self):
        return self.data.get("title")

    @classmethod
    async def get(cls, song, *, loop=None):
        loop = loop or asyncio.get_event_loop()
        data = loop.run_in_executor(None, lambda: ytdl.extract_info(song, False))

        if "entries" in data:
            data = data["entries"][0]
        return cls(discord.FFmpegPCMAudio(data["url"], **ffmpegopts), data=data)
