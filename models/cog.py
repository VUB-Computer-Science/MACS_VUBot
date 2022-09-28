import re
import os
import datetime

from discord.ext import commands
from discord.ext.commands import Context
from models.client import MaxVUBot


class CommandCog(commands.Cog):
    def __init__(self, ENVIRONMENT: list = None):
        self.ENVIRONMENT = ENVIRONMENT

    @commands.command()
    async def pls_pin(self, ctx: Context):
        message_reference: Optional[discord.MessageReference] = ctx.message.reference
        if not message_reference:
            await ctx.reply("Please use this command while replying on the message you wish to pin")
            return
        message_to_pin = message_reference.cached_message or await ctx.channel.fetch_message(
            message_reference.message_id
        )
        await message_to_pin.pin(reason=f"Pinned by {ctx.author}")
        await ctx.message.delete(delay=3)  # Deletes the request to pin after 3 seconds on command success

    @commands.command()
    async def pls_unpin(self, ctx: Context):
        message_reference: Optional[discord.MessageReference] = ctx.message.reference
        if not message_reference:
            await ctx.reply("Please use this command while replying on the message you wish to pin")
            return
        message_to_pin = message_reference.cached_message or await ctx.channel.fetch_message(
            message_reference.message_id
        )
        await message_to_pin.unpin()
        await ctx.message.delete(delay=3)  # Deletes the request to pin after 3 seconds on command success

    @commands.command()
    async def motd(self, ctx: Context):
        """
            Allows users to post once a day a Music Of The Day, that will become the topic of the main channel
        """
        last_change = os.environ.get("LAST_MOTD_CHANGE", None)
        if last_change is not None:
            last_change = datetime.datetime.fromisoformat(last_change)
            if datetime.datetime.now() - last_change < datetime.timedelta(days=1):
                await ctx.reply("You can only change the topic once a day")
                return
        os.environ["LAST_MOTD_CHANGE"] = datetime.datetime.now().isoformat()

        new_motd: str = ctx.message.content.replace("$motd ", "").strip()
        # This seems a bit overkill but hey, you know, security and stuff
        web_regex = re.compile(
            r"^(?:http|https):\/\/(?:[\w\.\-\+]+:{0,1}[\w\.\-\+]*@)?(?:[a-z0-9\-\.]+)(?::[0-9]+)?(?:\/|\/(?:[\w#!:\.\?\+=&%@!\-\/\(\)]+)|\?(?:[\w#!:\.\?\+=&%@!\-\/\(\)]+))?$"
        )
        if not web_regex.match(new_motd):
            await ctx.reply("Your Music Of The Day is not a valid url")
            return

        # Change topic, send a confirmation message and delete the command after 3 seconds
        await ctx.channel.edit(topic=f"MOTD: {new_motd} proposed by {ctx.message.author.mention}", reason=f"motd changed by {ctx.author}")
        await ctx.send(f"{ctx.message.author.mention}; You changed the motd to {new_motd} !")
        await ctx.message.delete(delay=3)  # Deletes the motd request after 3 seconds
