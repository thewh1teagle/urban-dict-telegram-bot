import requests
from bs4 import BeautifulSoup as BS
from telegram.ext import (
    Updater, 
    MessageHandler,
    Filters
)
from os import environ
from sys import argv


def urbandictionary(sentence: str) -> str:
    words = sentence.split(" ")
    print(words)
    result = requests.get("https://www.urbandictionary.com/define.php?term=" + '+'.join(words))
    if result.status_code != 200:
        return "Urban dictionary result: \nNot found!"
    else:
        try:
            soup = BS(result.text, features='html.parser')
            meaning = soup.findAll("div", {"class": "meaning"})
            return meaning[0].text
        except Exception as e:
            print(e)  # for debugging
            return "Urban dictionary result: \nNot found!"


def meaning_decorator(func: callable) -> callable:

    def wrapper(update, context):

        """Send a message when the command /start is issued."""
        message_text: str = update.message.text

        if message_text.startswith('.urban'):
            message_text: str = message_text.replace('.urban ', '')

        meaning = urbandictionary(message_text)
        update.message.reply_text(meaning)

        return meaning_decorator

    return wrapper


@meaning_decorator
def public(update, context):
    pass


@meaning_decorator
def private(update, context):
    pass


if __name__ == '__main__':
    
    try:
        bot_token = environ['BOT_TOKEN']
    except KeyError:
            print('No env bot token have been provieded.')
            print('Usage: export BOT_TOKEN=<BOT_TOKEN>')
            print('python3 {}'.format(argv[0]))
            exit(1)
    

    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater('1328418490:AAGrplpgEZQ19ZhtFPiaIWoOd98khWqiBOw', use_context=True)


    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(MessageHandler(filters=Filters.regex('^\.urban ') & ~Filters.private, callback=public))
    dp.add_handler(MessageHandler(filters=Filters.private & ~Filters.regex('^.urban '), callback=private))


    # Start the Bot
    print('Bot running')
    updater.start_polling()
    updater.idle()
