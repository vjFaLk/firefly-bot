#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that uses inline keyboards.
"""
import logging
import os
from pathlib import Path

from firefly import Firefly
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      ReplyKeyboardRemove)
from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, Filters, MessageHandler,
                          PicklePersistence, Updater)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

FIREFLY_URL, FIREFLY_TOKEN, DEFAULT_WITHDRAW_ACCOUNT = range(3)


def start(update, context):
    update.message.reply_text('Hi! Please enter your Firefly III URL')
    return FIREFLY_URL


def get_firefly_token(update, context):
    context.user_data['firefly_url'] = update.message.text
    update.message.reply_text('Hi! Please enter your Firefly III User Token')
    return DEFAULT_WITHDRAW_ACCOUNT


def get_default_account(update, context):
    token = update.message.text
    firefly = Firefly(hostname=context.user_data.get(
        "firefly_url"), auth_token=token)
    accounts = firefly.get_accounts(account_type="asset").get("data")

    accounts_keyboard = []
    for account in accounts:
        account_name = account.get("attributes").get("name")
        accounts_keyboard.append([InlineKeyboardButton(
            account_name, callback_data=account.get("id"))])

    reply_markup = InlineKeyboardMarkup(accounts_keyboard)

    context.user_data['firefly_token'] = update.message.text
    update.message.reply_text('Please choose:', reply_markup=reply_markup)
    return DEFAULT_WITHDRAW_ACCOUNT


def store_default_account(update, context):
    query = update.callback_query
    default_account_id = query.data
    context.user_data['firefly_default_account'] = default_account_id
    query.edit_message_text('Setup Complete. Happy Spending!(?)')
    return ConversationHandler.END

def spend(update, context):
    message = update.message.text.split(' ')

    if len(message) < 2:
        update.message.reply_text("Just type in an expense with a description. Like this - '5 Starbucks`")
        return

    amount = message[0]
    description = message[1]
    category = message[2] if 2 < len(message) else None # Safely try to check for index
    budget = message[3] if 3 < len(message) else None # Safely try to check for index
    
    firefly = get_firefly(context)
    account = context.user_data["firefly_default_account"]
    response = firefly.create_transaction(amount, description, account, category, budget)
    if response.status_code == 422:
        update.message.reply_text(response.get("message"))
    elif response.status_code == 200:
        update.message.reply_text("Transaction made successfully")
    else:
        update.message.reply_text("Something went wrong, check logs")



def about(update, context):
    firefly = get_firefly(context)
    about = firefly.get_about_user()
    update.message.reply_text("```{}```".format(about))

def get_firefly(context):
    return Firefly(hostname=context.user_data.get("firefly_url"), auth_token=context.user_data.get("firefly_token"))


def help(update, context):
    if not context.user_data.get('firefly_default_account'):
        update.message.reply_text("Type /start to initiate the setup process.")
    else:
        update.message.reply_text("""Just type in an expense with a description. \Like this - 
        \n '5 Starbucks' \n Additionally you can also include the category and budget (both optional)
        \n '5 Starbucks Coffee Food'""")


def cancel(update, context):
    update.message.reply_text('Cancelled')
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    data_dir = Path.joinpath(Path.home(), ".config", "firefly-bot")
    data_dir.mkdir(parents=True, exist_ok=True)
    bot_persistence = PicklePersistence(filename=str(data_dir/"bot-data"))
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    updater = Updater(bot_token,
                      persistence=bot_persistence, use_context=True)

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIREFLY_URL: [MessageHandler(Filters.text, get_firefly_token)],
            DEFAULT_WITHDRAW_ACCOUNT: [MessageHandler(Filters.text, get_default_account),
                                       CallbackQueryHandler(store_default_account, pattern='^[0-9]*$')]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('about', about))
    updater.dispatcher.add_handler(MessageHandler(filters=Filters.regex("^[0-9]+"), callback=spend))
    updater.dispatcher.add_error_handler(error)
    updater.dispatcher.add_handler(conversation_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
