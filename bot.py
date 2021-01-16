import logging
from config import token

from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, constants
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler,
                          CallbackQueryHandler, InlineQueryHandler, DictPersistence)

from models import User, engine, Base

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

NAME, AGE, CALL, QUESTION1, QUESTION2, QUESTION3, QUESTION4, QUESTION5, POLL, OPINION, PARTICIPATION, END = range(12)

cancel_keyboard = [[InlineKeyboardButton("لغو", callback_data='0')]]
refill_form = [[InlineKeyboardButton("پرکردن دوباره فرم", callback_data='1')]]


def create_keyboard(buttons):
    keyboard = [[]]
    i = 1
    for button in buttons:
        keyboard[0].append(InlineKeyboardButton(button, callback_data=i))
        i += 1
    return keyboard

def error(update, context, error):
    logger.warning('Update "%s" caused error "%s"', update, error)

def start(update, context):
    name = "برای شرکت در مسابقه، لطفا نام و نام خانوادگی خود را وارد بفرمایید."
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
    text = "لطفا پاسخ سوالات زیر را انتخاب فرمایید."
    update.message.reply_text(text)
    context.user_data['contact'] = update.message.text
    q1 = "میزان رضایت شما از فضای انتظار مراسم"
    q1_keys = create_keyboard(['رضایت کامل', 'رضایت نسبی', 'عدم رضایت'])
    update.message.reply_text(q1, reply_markup=InlineKeyboardMarkup(q1_keys))
    return QUESTION1

def wrong_contact(update, context):
    update.message.reply_text("شماره تماس خود را به درستی بنویسید. مثال: 09876543210")
    return CALL

def get_answer1(update, context):
    q2 = "میزان رضایت شما از محتوای مراسم"
    q2_keys = create_keyboard(['رضایت کامل', 'رضایت نسبی', 'عدم رضایت'])
    context.user_data['answer1'] = update.callback_query.data
    update.callback_query.message.reply_text(q2, reply_markup=InlineKeyboardMarkup(q2_keys))
    return QUESTION2

def get_answer2(update, context):
    q3 = "میزان رضایت شما از فضا و چیدمان سالن اصلی"
    q3_keys = create_keyboard(['رضایت کامل', 'رضایت نسبی', 'عدم رضایت'])
    context.user_data['answer2'] = update.callback_query.data
    update.callback_query.message.reply_text(q3, reply_markup=InlineKeyboardMarkup(q3_keys))
    return QUESTION3

def get_answer3(update, context):
    q4 = "میزان رضایت شما از نقالی و روایت گری"
    q4_keys = create_keyboard(['رضایت کامل', 'رضایت نسبی', 'عدم رضایت'])
    context.user_data['answer3'] = update.callback_query.data
    update.callback_query.message.reply_text(q4, reply_markup=InlineKeyboardMarkup(q4_keys))
    return QUESTION4

def get_answer4(update, context):
    q5 = "میزان رضایت شما از کلیت برنامه"
    q5_keys = create_keyboard(['رضایت کامل', 'رضایت نسبی', 'عدم رضایت'])
    context.user_data['answer4'] = update.callback_query.data
    update.callback_query.message.reply_text(q5, reply_markup=InlineKeyboardMarkup(q5_keys))
    return QUESTION5

def get_answer5(update, context):
    opinion = "انتقادات و پیشنهادات شما موجب پیشرفت سوگواره ی میراث فاطمی در برنامه های بعدی میباشد. چنانچه پیشنهاد یا انتقادی دارید، برای ما بنویسید."
    context.user_data['answer5'] = update.callback_query.data
    update.callback_query.message.reply_text(opinion, reply_markup=InlineKeyboardMarkup(cancel_keyboard))
    return OPINION

# def get_poll(update, context):
#     opinion = "انتقادات و پیشنهادات شما موجب پیشرفت سوگواره ی میراث فاطمی در برنامه های بعدی میباشد. چنانچه پیشنهاد یا انتقادی دارید، برای ما بنویسید."
#     context.user_data['poll'] = update.message.text
#     update.message.reply_text(opinion, reply_markup=InlineKeyboardMarkup(cancel_keyboard))
#     return OPINION

# def wrong_poll(update, context):
#     update.message.reply_text("پاسخ را به درستی بنویسید.")
#     return POLL

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
    answer1 = context.user_data['answer1']
    answer2 = context.user_data['answer3']
    answer3 = context.user_data['answer4']
    answer4 = context.user_data['answer2']
    answer5 = context.user_data['answer5']
    opinion = context.user_data['opinion']
    user = User(name, age, phone_number, answer1, answer2, answer3, answer4, answer5, opinion, participation)
    user.add(user)
    return END


def bot():
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            NAME: [MessageHandler(Filters.text, get_name), MessageHandler(~Filters.text, wrong_name)],
            AGE: [MessageHandler(Filters.regex(r'^[۱۲۳۴۵۶۷۸۹۰0-9]{1,3}$'), get_age), MessageHandler(~Filters.regex(r'^[۱۲۳۴۵۶۷۸۹۰0-9]{1,3}$'), wrong_age)],
            CALL: [MessageHandler(Filters.regex(r'^[۱۲۳۴۵۶۷۸۹۰0-9]{11}$'), get_contact), MessageHandler(~Filters.regex(r'^[۱۲۳۴۵۶۷۸۹۰0-9]{11}$'), wrong_contact)],
            QUESTION1: [CallbackQueryHandler(get_answer1, pattern=r'1|2|3')],
            QUESTION2: [CallbackQueryHandler(get_answer2, pattern=r'1|2|3')],
            QUESTION3: [CallbackQueryHandler(get_answer3, pattern=r'1|2|3')],
            QUESTION4: [CallbackQueryHandler(get_answer4, pattern=r'1|2|3')],
            QUESTION5: [CallbackQueryHandler(get_answer5, pattern=r'1|2|3')],
            # POLL: [MessageHandler(Filters.regex(r'[۱۲۳۴۵۶۷۸۹۰0-9]{5}'), get_poll), MessageHandler(~Filters.regex(r'[۱۲۳۴۵۶۷۸۹۰0-9]{5}'), wrong_poll)],
            OPINION: [MessageHandler(Filters.text, get_opinion), CallbackQueryHandler(get_opinion, pattern=r'0')],
            PARTICIPATION: [MessageHandler(Filters.text, get_participation), CallbackQueryHandler(get_participation, pattern=r'0')],
            END: [CommandHandler('start', start)]
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