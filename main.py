import json
import logging

import coloredlogs
from hereby import Here

from models.client import MaxVUBot

if __name__ == "__main__":
    here = Here(__file__)

    coloredlogs.install()
    logging.basicConfig(
        level=logging.DEBUG,
    )

    with open(here.abspath(".env.json")) as key:
        API_KEY = json.load(key).get("API_KEY", None)

    if API_KEY is None:
        logging.error("No API key found ! quitting")
    else:
        client = MaxVUBot.get_instance()

        client.run(API_KEY)
