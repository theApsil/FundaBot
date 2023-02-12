import telebot
from telebot import types
# token: 6131203698:AAH0vXX_8YuTzENkHTamN7TWSYktiboBPJE
bot = telebot.TeleBot("6131203698:AAH0vXX_8YuTzENkHTamN7TWSYktiboBPJE")


@bot.message_handler(commands=['start'])
def start(message):
    sMess = f'<b>Привет, {message.from_user.first_name} {message.from_user.last_name} я - FundaBot</b>'
    bot.send_message(message.chat.id, sMess, parse_mode='html')
    bot.send_message(message.chat.id, '<b> Вот список моих комманд </b>', parse_mode='html')
    bot.send_message(message.chat.id,
                     '<b>1. Лабораторная работа 2.1\n'
                     '2. Лабораторная работа 2.2\n'
                     '3. Лабораторная работа 2.3\n'
                     '4. Лабораторная работа 2.4\n'
                     '5. Курсовая работа по ФСДИА</b>',
                     parse_mode='html')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    btn1 = types.KeyboardButton("2.1")
    btn2 = types.KeyboardButton("2.2")
    btn3 = types.KeyboardButton("2.3")
    btn4 = types.KeyboardButton("2.4")
    btn5 = types.KeyboardButton("Курсовая работа")
    markup.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(message.chat.id, "Что ты хочешь посмотреть?", reply_markup=markup)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Временно недоступно")


bot.polling(none_stop=True)
