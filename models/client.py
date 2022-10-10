import logging

import discord
import emoji
from discord import MessageType
from discord.ext import commands
from discord_slash import SlashCommand


class MaxVUBot(commands.Bot):
    """MaxVUBot's client"""

    instance = None

    @staticmethod
    def get_instance():
        """Singleton Pattern"""
        if MaxVUBot.instance is None:
            MaxVUBot()
        return MaxVUBot.instance

    def __init__(self):
        if MaxVUBot.instance is not None:
            raise RuntimeError(f"Trying to instanciate a second object of {__class__}")
        MaxVUBot.instance = self

        intents = discord.Intents.default()
        intents.members = True
        intents.presences = True
        intents.reactions = True

        super().__init__(command_prefix="$", intents=intents)

        self.slash = SlashCommand(self, sync_commands=True)

    async def on_ready(self):
        """This is called when the connection to disord's API is established"""
        logging.info(f"Logged on as {self.user}!")
        await self.change_presence(
            status=discord.Status.idle, activity=discord.Game("Sorting out how to make new friends")
        )

    async def on_raw_reaction_add(self, payload):
        """Callback for reaction adding non chache-dependent"""
        if emoji.demojize(str(payload.emoji)) == ":pushpin:":
            logging.info("pinning message")
            channel = self.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            if message.type == MessageType.default:
                await message.pin(reason=f"Pinned by {payload.member}")
            else:
                logging.info(f"Tried to ping message of type {message.type}")
                await channel.send(f"{payload.member.mention} I can't pin system messages !")

    async def on_raw_reaction_remove(self, payload):
        """Callback for reaction removing non chache-dependent"""
        if emoji.demojize(str(payload.emoji)) == ":pushpin:":
            logging.info(f"Triggered the unpinning of message {payload.message_id}")
            channel = self.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            if message.type == MessageType.default:
                await message.unpin()
