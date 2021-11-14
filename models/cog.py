from discord.ext import commands

from discord.ext.commands import Context
from models.client import MaxVUBot


class CommandCog(commands.Cog):
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
