# Firefly Bot

A Telegram bot to create transactions in Firefly III. As of now it only does one thing - create transactions

## Installation

First you'll have to generate a Telegram Bot token through [BotFather](https://t.me/botfather). Once you generate the token, keep it safe.

### Docker (Recommended)

```bash
docker create \
  --name=firefly-bot \ 
  -e TELEGRAM_BOT_TOKEN=<your-bot-token> \
  -v </path/to/config>:/config \
  vjfalk1/firefly-telegram-bot
```

### Local
You'll need python 3.8 and pip installed

- Clone the repository
- Install dependencies by running `pip install -r requirements.txt`
- Run `export FIREFLY_BOT_TOKEN=<your-bot-token>`
- Run `python3 ./src/bot.py`

---

## Usage

### Creating Transactions
- Once the bot is up and running, type in `/start` in Telegram and follow the instructions
- Create a new Transaction like this - `Amount Description Category Budget`
  - Category and Budget are both optional
- Example - `5 Starbucks Coffee Food`

### Limitations
- You can't include a budget without having to include a cateogory as well. This is because of the hard-coded syntax.

---

## Development
- Clone the repository
- Install [Poetry](https://github.com/python-poetry/poetry)
- Install dependencies by running `poetry install`
- Run `poetry shell` to activate virtualenv

### Notes

**Why Poetry AND requirements.txt?**
I don't want to use poetry inside Docker. It's unnecessary bloat and complexity. So I just generate a requirements.txt anytime I change deps using - `poetry export -f requirements.txt > requirements.txt`. It can then be used for Docker, or just anyone who wants to use this without having to install (and figure out) poetry.