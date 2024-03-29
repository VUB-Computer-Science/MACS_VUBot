import json
import logging

import coloredlogs
from hereby import Here

from models.client import MaxVUBot
from models.cog import CommandCog

if __name__ == "__main__":
    here = Here(__file__)

    coloredlogs.install()
    logging.basicConfig(
        level=logging.INFO,
    )

    with open(here.abspath(".env.json")) as key:
        ENVIRONMENT = json.load(key)
        API_KEY = ENVIRONMENT.get("API_KEY", None)

    if API_KEY is None:
        logging.error("No API key found ! quitting")
    else:
        client = MaxVUBot.get_instance()
        client.add_cog(CommandCog(ENVIRONMENT=ENVIRONMENT))
        logging.info(f"Starting application with env vars: {', '.join(ENVIRONMENT.keys())}")
        client.run(API_KEY)
