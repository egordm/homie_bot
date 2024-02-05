# Discord Homie Bot
A simple framework creating Discord LLM bots with a customized persona and a few world building commands.

## Features
* Customizable persona using markdown and chat examples.
* Lore commands and packing them into the bot based on text match.
* Server member backstories
* Administration commands like `$regnerate`, `$reset`, and `$purge` 

Discord Help Text:
```
No Category:
  backstory     View the backstory for a character. Yours by default.
  backstory_set Changes backstory for your character
  help          Shows this message
  lore_add      Creates a lore entry
  lore_delete   Deletes a lore entry
  lore_list     Lists all lore entries
  lore_view     View a lore entry
  purge         Purge n messages from the channel
  regenerate    Regenerates last message in the channel.
  reset         Resets the bot memory. All messages before this command will...

Type $help command for more info on a command.
You can also type $help category for more info on a category.
```

Use `!text` to make the bot ignore the message.

## Requirements
* For local LLM:
    * [Ollama](https://github.com/ollama/ollama)
    * Python 3.10 (or higher)
* For API LLM: Not yet implemented, do it yourself in `homie_bot/chatting/llm.py`

## Installation
Install the required packages using pip:
```bash
pip install -r requirements.txt
# or if you prefer poetry
poetry install
```

Register your bot on the [Discord Developer Portal](https://discord.com/developers/applications) and get the bot token.

For a comprehensive guide on register a bot, see the [Creating a Bot Account](https://discordpy.readthedocs.io/en/stable/discord.html).

Invite the bot to your server using the following link:
```
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=2147871808&scope=bot
```

Create a `.env` file from the `.env.example` and fill in the required fields. Make sure that you have a channel in your server with the same name as `CHANNEL_NAME` key in your `.env`.

Start the bot using the following command:
```bash
python bot.py
```

## Customization
The bot persona configuration is stored in `bots/bot_name/*.md`. See Homie Bot for an example at [bots/Homie](bots/Homie).