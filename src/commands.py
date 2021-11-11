import discord

from models.command_registry import CommandRegistry

registry = CommandRegistry.get_instance()


@registry.register(command="hi", description="Say hello", help="...")
async def greet(
    user: discord.Member, guild: discord.Guild, channel: discord.channel, command: list, initial: discord.Message
):
    await channel.send(f"Hello {user.mention}")
