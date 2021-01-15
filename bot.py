import logging
from config import token

from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, constants
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler,
                          CallbackQueryHandler, InlineQueryHandler, DictPersistence)

from models import User, engine, Base

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

NAME, AGE, CALL, QUESTION, POLL, OPINION, PARTICIPATION, END = range(8)

cancel_keyboard = [[InlineKeyboardButton("لغو", callback_data='0')]]

def error(update, context, error):
    logger.warning('Update "%s" caused error "%s"', update, error)

def start(update, context):
    name = "سلام، به ربات تلگرامی سوگواره میراث فاطمی خوش آمدید. برای شرکت در مسابقه، لطفا نام و نام خانوادگی خود را وارد بفرمایید."
    update.message.reply_text(name)
    return NAME

def get_name(update, context):
    age = "سن خود را وارد بفرمایید."
    context.user_data['name'] = update.message.text
    update.message.reply_text(age)
    return AGE

def wrong_name(update, context):
    update.message.reply_text("نام و نام خانوادگی خود را به درستی بنویسید.")
    return NAME

def get_age(update, context):
    contact = "شماره تماس(تلفن همراه) خود را وارد بفرمایید. مثال: 09876543210"
    context.user_data['age'] = update.message.text
    update.message.reply_text(contact)
    return CALL

def wrong_age(update, context):
    update.message.reply_text("سن خود را به درستی بنویسید.")
    return AGE

def get_contact(update, context):
    answer = "پاسخ مسابقه ی میراث فاطمی را به صورت یک عدد 5 رقمی وارد بفرمایید."
    context.user_data['contact'] = update.message.text
    update.message.reply_text(answer)
    return QUESTION

def wrong_contact(update, context):
    update.message.reply_text("شماره تماس خود را به درستی بنویسید. مثال: 09876543210")
    return CALL


def get_answer(update, context):
    poll = "پاسخ سوال نظر سنجی را به صورت یک عدد 5 رقمی وارد وارد بفرمایید."
    context.user_data['answer'] = update.message.text
    update.message.reply_text(poll)
    return POLL

def wrong_answer(update, context):
    update.message.reply_text("پاسخ را به درستی بنویسید.")
    return QUESTION

def get_poll(update, context):
    opinion = "انتقادات و پیشنهادات شما موجب پیشرفت سوگواره ی میراث فاطمی در برنامه های بعدی میباشد. چنانچه پیشنهاد یا انتقادی دارید، برای ما بنویسید."
    context.user_data['poll'] = update.message.text
    update.message.reply_text(opinion, reply_markup=InlineKeyboardMarkup(cancel_keyboard))
    return OPINION

def wrong_poll(update, context):
    update.message.reply_text("پاسخ را به درستی بنویسید.")
    return POLL

def get_opinion(update, context):
    participation = "سوگواره ی میراث فاطمی با کمک های شما برقرار میباشد؛چنانچه تمایل به همکاری در برگزاری مراسم های بعدی دارید، زمینه ی همکاری را بفرمایید (مثلا انتظامات ،خدمات صوت، خدمات عکاسی و...)"
    if not update.message:
        update = update.callback_query
        update.message.reply_text(participation, reply_markup=InlineKeyboardMarkup(cancel_keyboard))
    else:
        update.message.reply_text(participation, reply_markup=InlineKeyboardMarkup(cancel_keyboard))
    context.user_data['opinion'] = update.message.text
    return PARTICIPATION


def get_participation(update, context):
    bye = "ممنون از شما. عزاداری ها مورد قبول صاحب عزا قرار بگیرد. قرعه کشی همزمان با ولادت حضرت زهرا سلام الله علیها برگزار خواهد شد و از طریق همین ربات تلگرامی نتیجه به اطلاع شما خواهد رسید."
    if not update.message:
        update = update.callback_query
        update.message.reply_text(bye)
    else:
        update.message.reply_text(bye)
    participation = update.message.text
    name = context.user_data['name']
    age = context.user_data['age']
    phone_number = context.user_data['contact']
    answer = context.user_data['answer']
    poll = context.user_data['poll']
    opinion = context.user_data['opinion']
    user = User(name, age, phone_number, answer, poll, opinion, participation)
    user.add(user)
    return END


def bot():
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            NAME: [MessageHandler(Filters.text, get_name), MessageHandler(~Filters.text, wrong_name)],
            AGE: [MessageHandler(Filters.regex(r'[0-9]{1,2}'), get_age), MessageHandler(~Filters.regex(r'[0-9]{1,2}'), wrong_age)],
            CALL: [MessageHandler(Filters.regex(r'[0-9]{10}'), get_contact), MessageHandler(~Filters.regex(r'[0-9]{10}'), wrong_contact)],
            QUESTION: [MessageHandler(Filters.regex(r'[0-9]{5}'), get_answer), MessageHandler(~Filters.regex(r'[0-9]{5}'), wrong_answer)],
            POLL: [MessageHandler(Filters.regex(r'[0-9]{5}'), get_poll), MessageHandler(~Filters.regex(r'[0-9]{5}'), wrong_poll)],
            OPINION: [MessageHandler(Filters.text, get_opinion), CallbackQueryHandler(get_opinion, pattern=r'0')],
            PARTICIPATION: [MessageHandler(Filters.text, get_participation), CallbackQueryHandler(get_participation, pattern=r'0')]
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