"""
Cog for meme commands.
"""

from random import choice

import disnake
from disnake.ext import commands

import utils
from cogs.base import Base
from config import cooldowns
from config.app_config import config
from config.messages import Messages

uhoh_counter = 0


class Meme(Base, commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: disnake.message):
        global uhoh_counter

        if message.author.bot:
            if (
                message.author.id in config.grillbot_ids
                and message.content.startswith("<:")
                and message.content.endswith(">")
            ):
                await message.channel.send(message.content)
            return

        elif config.uhoh_string in message.content.lower():
            await message.channel.send("uh oh")
            uhoh_counter += 1
        elif message.content == "PR":
            await message.channel.send(Messages.pr_meme)

    @commands.slash_command(name="uhoh", description=Messages.uhoh_brief)
    async def uhoh(self, inter):
        await inter.send(utils.fill_message("uhoh_counter", uhohs=uhoh_counter))

    # Ignore '??'
    @commands.command(name="?")
    async def ignore_questionmark(self, ctx):
        pass

    @cooldowns.short_cooldown
    @commands.command(name="??", brief="???")
    async def question(self, ctx):
        await ctx.send(choice(Messages.question))


def setup(bot):
    bot.add_cog(Meme(bot))
