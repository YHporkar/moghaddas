import logging
from config import token

from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, constants
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler,
                          CallbackQueryHandler, InlineQueryHandler, DictPersistence)

from models import User, engine

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

NAME, AGE, CALL, QUESTION, POLL, CRITIC, PARTICIPATION, END = range(9)

def error(update, context, error):
    logger.warning('Update "%s" caused error "%s"', update, error)

def start(update, context):
    update.message.reply_text('welcome! send your name')
    return NAME

def get_name(update, context):
    context.user_data['name'] = update.message.text
    update.message.reply_text('send your age')
    return AGE

def get_age(update, context):
    context.user_data['age'] = update.message.text
    update.message.reply_text('send your phonenumber')
    return CALL

def get_contact(update, context):
    context.user_data['contact'] = update.message.text
    update.message.reply_text('send your answer')
    return QUESTION

def get_answer(update, context):
    context.user_data['answer'] = update.message.text
    update.message.reply_text('send your poll')
    return POLL

def get_poll(update, context):
    context.user_data['poll'] = update.message.text
    update.message.reply_text('send your critic')
    return CRITIC

def get_critic(update, context):
    context.user_data['critic'] = update.message.text
    update.message.reply_text('send your participation')
    return PARTICIPATION

def get_participation(update, context):
    context.user_data['participation'] = update.message.text
    update.message.reply_text('bye')
    return END


def bot():
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            NAME: [MessageHandler(Filters.text, get_name)],
            AGE: [MessageHandler(Filters.regex(r'[0-9]+'), get_age)],
            CALL: [MessageHandler(Filters.regex(r'[0-9]+'), get_contact)],
            QUESTION: [MessageHandler(Filters.regex(r'[0-9]{5}'), get_answer)],
            POLL: [MessageHandler(Filters.regex(r'[0-9]{5}'), get_poll)],
            CRITIC: [MessageHandler(Filters.regex(r'[A-Za-z0-9]+'), get_critic)],
            PARTICIPATION: [MessageHandler(Filters.regex(r'[A-Za-z0-9]+'), get_participation)]
        },
        fallbacks=[
            CommandHandler('cancel', start)
        ]
    )

    dp.add_handler(conv_handler)
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    bot()