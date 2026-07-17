# Michael Bot

A Discord bot built with [discord.py](https://discordpy.readthedocs.io/).

## Setup

### 1. Install uv

```sh
brew install uv
```

### 2. Install dependencies

```sh
uv sync
```

### 3. Configure environment

You will need an owner-provided `.env` file in the project root for this bot to work

## Running

```sh
uv run bot           # start the bot
uv run bot-sync      # start the bot and sync slash commands with Discord
uv run bot-notify    # start the bot and send a startup message to the main channel
```

## Utility Scripts

```sh
uv run clear-db       # interactively clear the database
uv run add-box-item   # interactively add an item to the mystery box
uv run update-box-db  # rebuild the flat item index from typed box data
```
