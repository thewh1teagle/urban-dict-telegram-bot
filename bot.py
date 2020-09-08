import requests
from bs4 import BeautifulSoup as BS
from telegram.ext import (
    Updater, 
    MessageHandler
)
from os import environ
from sys import argv



def urbandictionary(word: str):
    result = requests.get("https://www.urbandictionary.com/define.php?term=" + word)
    if result.status_code != 200:
        #raise('Not found')
        print('not found')
    else:
        try:
            soup = BS(result.text, features='html.parser')
            meaning = soup.findAll("div", {"class": "meaning"})
            return meaning[0].text
        except Exception as e:
            print(e)
            #raise('not found')




def message_handler(update, context):
    """Send a message when the command /start is issued."""
    message_text = update.message.text
    if message_text.startswith('.urban') and len(message_text.split()) == 2:
        text = message_text.split()[1]
        meaning = urbandictionary(text)
        if meaning:
            update.message.reply_text("Urban dictionary result: \n{}".format(meaning))
        else:
            update.message.reply_text("Urban dictionary result: \nNot found!")
        
        
        




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
    updater = Updater(bot_token, use_context=True)


    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(MessageHandler(filters=None, callback=message_handler))


    # Start the Bot
    print('Bot running')
    updater.start_polling()
    updater.idle()
