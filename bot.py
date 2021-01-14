import logging
from config import token

from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, constants
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler,
                          CallbackQueryHandler, InlineQueryHandler, DictPersistence)

from models import User, engine, Base

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

NAME, AGE, CALL, QUESTION, POLL, CRITIC, PARTICIPATION, END = range(8)

def error(update, context, error):
    logger.warning('Update "%s" caused error "%s"', update, error)

def start(update, context):
    update.message.reply_text("Welcome. send your name")
    return NAME

def get_name(update, context):
    context.user_data['name'] = update.message.text
    update.message.reply_text('send your age')
    return AGE

def wrong_name(update, context):
    update.message.reply_text('wrong name, again:')
    return NAME

def get_age(update, context):
    context.user_data['age'] = update.message.text
    update.message.reply_text('send your phonenumber')
    return CALL

def wrong_age(update, context):
    update.message.reply_text('wrong age, again:')
    return AGE

def get_contact(update, context):
    context.user_data['contact'] = update.message.text
    update.message.reply_text('send your answer')
    return QUESTION

def wrong_number(update, context):
    update.message.reply_text('wrong number, again:')
    return CALL


def get_answer(update, context):
    context.user_data['answer'] = update.message.text
    update.message.reply_text('send your poll')
    return POLL

def wrong_answer(update, context):
    update.message.reply_text('wrong answer, again:')
    return QUESTION

def get_poll(update, context):
    context.user_data['poll'] = update.message.text
    update.message.reply_text('send your critic')
    return CRITIC

def wrong_poll(update, context):
    update.message.reply_text('wrong poll, again:')
    return POLL

def get_critic(update, context):
    context.user_data['critic'] = update.message.text
    update.message.reply_text('send your participation')
    return PARTICIPATION

def wrong_critic(update, context):
    update.message.reply_text('wrong opinion, again:')
    return CRITIC

def get_participation(update, context):
    name = context.user_data['name']
    age = context.user_data['age']
    phone_number = context.user_data['contact']
    answer = context.user_data['answer']
    poll = context.user_data['poll']
    opinion = context.user_data['critic']
    participation = update.message.text
    user = User(name, age, phone_number, answer, poll, opinion, participation)
    user.add(user)
    update.message.reply_text('bye')
    return END

def wrong_participation(update, context):
    update.message.reply_text('wrong participation, again:')
    return PARTICIPATION

def bot():
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            NAME: [MessageHandler(Filters.text, get_name), MessageHandler(~Filters.text, wrong_name)],
            AGE: [MessageHandler(Filters.regex(r'[0-9]+'), get_age), MessageHandler(~Filters.regex(r'[0-9]+'), wrong_age)],
            CALL: [MessageHandler(Filters.regex(r'[0-9]+'), get_contact), MessageHandler(~Filters.regex(r'[0-9]+'), wrong_number)],
            QUESTION: [MessageHandler(Filters.regex(r'[0-9]{5}'), get_answer), MessageHandler(~Filters.regex(r'[0-9]{5}'), wrong_answer)],
            POLL: [MessageHandler(Filters.regex(r'[0-9]{5}'), get_poll), MessageHandler(~Filters.regex(r'[0-9]{5}'), wrong_poll)],
            CRITIC: [MessageHandler(Filters.regex(r'[A-Za-z0-9]+'), get_critic), MessageHandler(~Filters.regex(r'[A-Za-z0-9]+'), wrong_critic)],
            PARTICIPATION: [MessageHandler(Filters.regex(r'[A-Za-z0-9]+'), get_participation), MessageHandler(~Filters.regex(r'[A-Za-z0-9]+'), wrong_participation)]
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