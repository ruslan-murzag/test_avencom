from db import connect_sql
import pandas as pd
import telebot

conn, cursor = connect_sql('db_avencom', 'user_avencom', '', 'localhost')
cursor.callproc('auto_report')

result = cursor.fetchall()
df = pd.DataFrame(result, columns=['Brand', 'Model', 'Year', 'AVG Price', 'Min Price', 'Max Price', 'Amount'])
df.to_excel('output.xlsx')

conn.commit()

cursor.close()
conn.close()

Token = ''
bot = telebot.TeleBot(Token)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    doc = open('output.xlsx', 'rb')

    bot.send_document(message, doc)


bot.infinity_polling()
