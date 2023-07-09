from db import connect_sql
import pandas as pd
import telebot
from telebot import types

Token = ''
bot = telebot.TeleBot(Token)


def make_xlsx():
    conn, cursor = connect_sql('db_avencom', 'user_avencom', '', 'localhost')
    cursor.callproc('auto_report')

    result = cursor.fetchall()
    df = pd.DataFrame(result, columns=['Brand', 'Model', 'Year', 'AVG Price', 'Min Price', 'Max Price', 'Amount'])
    df.to_excel('output.xlsx')

    conn.commit()

    cursor.close()
    conn.close()


@bot.message_handler(commands=['start'])
def url(message):
    make_xlsx()
    file = open('output.xlsx', 'rb')
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Наш сайт', url='https://habr.com/ru/all/')
    markup.add(btn1)
    bot.send_message(message.from_user.id, "По кнопке ниже можно перейти на сайт хабра", reply_markup = markup)
    bot.send_document(message.chat.id, document=file)
    print(message.chat.id)


def send_rep_users():
    ids = ['545620069']
    file = open('output.xlsx', 'rb')
    for id in ids:
        bot.send_document(id, document=file)



bot.infinity_polling()

