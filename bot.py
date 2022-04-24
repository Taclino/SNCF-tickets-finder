from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from tickets_finder import *


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    chat_id = update.message.chat_id
    update.message.reply_text('Hi! I am looking for ' +
                              'tickets from ' + departure_station_name + ' to ' +
                              arrival_station_name + ' on date ' + day_of_departure + ".\n\n" +
                              'Every few minutes, I do an online scan : ' +
                              'if I find one, I notify you.\n\nYou can ' +
                              'still do /tickets to have an immediate result ! \U0001f603')
    context.job_queue.run_repeating(loop_tickets, interval=look_interval,  # in seconds
                                    first=0, context=chat_id, job_kwargs=None)


def loop_tickets(context):
    job = context.job
    nb_tickets, best_price = look_for_tickets()
    if nb_tickets > 0:
        context.bot.send_message(job.context, text='Found ' +
                                 str(nb_tickets) + ' tickets starting at ' +
                                 str(best_price) + '€ with carte avantage jeune ! \U0001f603')


def tickets(update, context):

    nb_tickets, best_price = look_for_tickets()
    if nb_tickets > 0:
        update.message.reply_text('\U0001f3ab Found ' +
                                  str(nb_tickets) + ' tickets starting at ' +
                                  str(best_price) + '€ with carte avantage jeune on date ' + day_of_departure + ' ! \U0001f603')
    else:
        update.message.reply_text('\U0000274c ' +
                                  'No tickets found on date ' + day_of_departure + '. \U0001f622')


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(bot_token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("tickets", tickets))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
