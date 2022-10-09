import datetime
import logging
import os
import re
from typing import Optional

import discord
from discord.ext import commands
from discord.ext.commands import Context

logger = logging.getLogger(__name__)


class CommandCog(commands.Cog):
    def __init__(self, ENVIRONMENT: list = None):
        self.ENVIRONMENT = ENVIRONMENT

    @commands.command()
    async def pls_pin(self, ctx: Context):
        """
        Pins the referenced message to the channel
        """
        logger.info(f"Received command pls_pin from {ctx.author}")
        message_reference: Optional[discord.MessageReference] = ctx.message.reference
        if not message_reference:
            logger.error("The command pls_pin was used without a message reference")
            await ctx.reply("Please use this command while replying on the message you wish to pin")
            return
        message_to_pin = message_reference.cached_message or await ctx.channel.fetch_message(
            message_reference.message_id
        )
        await message_to_pin.pin(reason=f"Pinned by {ctx.author}")
        logger.info("The message was successfully pinned")
        await ctx.message.delete(delay=3)  # Deletes the request to pin after 3 seconds on command success

    @commands.command()
    async def pls_unpin(self, ctx: Context):
        """
        Unpins the message referenced by the command
        """
        logger.info(f"Received command pls_unpin from {ctx.author}")
        message_reference: Optional[discord.MessageReference] = ctx.message.reference
        if not message_reference:
            logger.error("The command pls_unpin was used without a message reference")
            await ctx.reply("Please use this command while replying on the message you wish to pin")
            return
        message_to_pin = message_reference.cached_message or await ctx.channel.fetch_message(
            message_reference.message_id
        )
        await message_to_pin.unpin()
        logger.info("The message was successfully unpinned")
        await ctx.message.delete(delay=3)  # Deletes the request to unpin after 3 seconds on command success

    @commands.command()
    async def motd(self, ctx: Context):
        """
        Allows users to post once a day a Music Of The Day, that will become the topic of the main channel
        """
        logger.info(f"Received command motd from {ctx.author}")
        last_change = os.environ.get("LAST_MOTD_CHANGE", None)
        if last_change is not None:
            last_change = datetime.datetime.fromisoformat(last_change)
            if datetime.datetime.now().day() == last_change.day():
                logger.error("The command motd was used twice in the same day")
                await ctx.reply("You can only change the topic once a day")
                return

        new_motd: str = ctx.message.content.replace("$motd ", "").strip()
        # This seems a bit overkill but hey, you know, security and stuff
        web_regex = re.compile(
            r"^(?:http|https):\/\/(?:[\w\.\-\+]+:{0,1}[\w\.\-\+]*@)?(?:[a-z0-9\-\.]+)(?::[0-9]+)?(?:\/|\/(?:[\w#!:\.\?\+=&%@!\-\/\(\)]+)|\?(?:[\w#!:\.\?\+=&%@!\-\/\(\)]+))?$"  # noqa
        )
        if not web_regex.match(new_motd):
            logger.error(f"The command motd was used with an invalid url: {new_motd}")
            await ctx.reply("Your Music Of The Day is not a valid url")
            return

        # Check that the environment variable is set
        if self.ENVIRONMENT is not None and self.ENVIRONMENT.get("MOTD_CHANNEL", None) is None:
            logger.error("The command motd was used but the environment variable MOTD_CHANNEL is not set")
            await ctx.reply("The MOTD channel is not set up, please contact the bot host")
            return

        motd_channel = ctx.guild.get_channel(self.ENVIRONMENT["MOTD_CHANNEL"])  # MOTD channel

        # Change topic, send a confirmation message and delete the command after 3 seconds
        await motd_channel.edit(
            topic=f"MOTD: {new_motd} proposed by {ctx.message.author.mention}", reason=f"motd changed by {ctx.author}"
        )
        await ctx.send(f"{ctx.message.author.mention}; You changed the motd to {new_motd} !")
        logger.info("MOTD changed successfully")

        os.environ["LAST_MOTD_CHANGE"] = datetime.datetime.now().isoformat()
        logger.info("Updating the last update date")
        await ctx.message.delete(delay=3)  # Deletes the motd request after 3 seconds
