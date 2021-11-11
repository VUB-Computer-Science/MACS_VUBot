import discord

from discord_slash import SlashCommand

from src.parser import parse_command
from models.command_registry import CommandRegistry


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

        import src.commands  # NOQA

        self.slash = SlashCommand(self, sync_commands=True)
        self.registry = CommandRegistry.get_instance()

    async def on_ready(self):
        """This is called when the connection to disord's API is established"""
        logging.info(f"Logged on as {self.user}!")
        await self.change_presence(
            status=discord.Status.idle, activity=discord.Game("Sorting out how to make new friends")
        )

    async def on_message(self, message: discord.Message):
        """Called when a message is sent womewhere the bot can access"""
        if message.content and message.content[0] == "$":
            params = await parse_command(message)
            command = self.registry.get(params["command"]["command"])
            await command(**params)
