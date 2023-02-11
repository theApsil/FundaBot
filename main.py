import telebot

# token: 6131203698:AAH0vXX_8YuTzENkHTamN7TWSYktiboBPJE
bot = telebot.TeleBot("6131203698:AAH0vXX_8YuTzENkHTamN7TWSYktiboBPJE")


@bot.message_handler(commands=['start'])
def start(message):
    sMess = f'<b>Привет, {message.from_user.first_name} {message.from_user.last_name} я - FundaBot</b>'
    bot.send_message(message.chat.id, sMess, parse_mode='html')
    bot.send_message(message.chat.id, 'Напиши <b>/help</b> и увидишь список комманд', parse_mode='html')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id,
                     '<b>Список моих функций:</b>\n'
                     '<i>1. Лабораторная работа 2.1\n'
                     '2. Лабораторная работа 2.2\n'
                     '3. Лабораторная работа 2.3\n'
                     '4. Лабораторная работа 2.4\n'
                     '5. Курсовая работа по ФСДИА</i>',
                     parse_mode='html')


bot.polling(none_stop=True)
