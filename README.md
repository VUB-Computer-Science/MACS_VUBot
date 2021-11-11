# MAX Vubot

A simple collaborative bot for the VUB's computer science master's discord.

## Development
This project requires poetry python package manager to be installed.

Once the repository is cloned, simply run
```bash
# To install dependencies and create a virtualenv
poetry install

# To activate virtualenv
poetry shell

# To run the project, simply type
python3 main.py

# to exit virtualenv
exit
```

You'll need a file named `.env.json` contianing the API key in order to run the bot.
the file should look like :
```json
{
    "API_KEY": "YOUR_API_KEY_HERE"
}
```
