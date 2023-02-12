import telebot
from dataclasses import dataclass
from telebot import types
# token: 6131203698:AAH0vXX_8YuTzENkHTamN7TWSYktiboBPJE
bot = telebot.TeleBot("6131203698:AAH0vXX_8YuTzENkHTamN7TWSYktiboBPJE")

@dataclass
class UserInfo:
    user_id: int
    task: str = None  # Задание (номер лабы или курсач)
    description: str = None  # Описание задания (всякие ограничения и предметная область)

# Сюда будут добавляться пользователи, совершившие заказ
users_info: dict[int, UserInfo] = dict()  # user_id : UserInfo

start_buttons_labels = [
    "2.1 (Поиск в строке)",
    "2.2 (Поиск в массиве)",
    "2.3 (Хеш-Таблицы)",
    "2.4 (Графы)",
    "Курсовая работа",
]


"""/start"""
@bot.message_handler(commands=['start'])
def start(message: types.Message):
    sMess = f'<b>Привет, {message.from_user.first_name} {message.from_user.last_name}, я - FundaBot</b>'
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
    btns = []
    for btn_label in start_buttons_labels:
        btn = types.KeyboardButton(text=btn_label)
        btns.append(btn)
    markup.add(*btns)
    bot.send_message(message.chat.id, "Что ты хочешь посмотреть?", reply_markup=markup)


"""/help"""
@bot.message_handler(commands=['help'])
def help(message: types.Message):
    bot.send_message(message.chat.id, "Временно недоступно")


"""/get_users - возвращает users_info для дебага"""
@bot.message_handler(commands=["get_users"])
def get_users(message: types.Message):
    bot.send_message(message.chat.id, str(users_info))


"""Обработчик всех стартовых кнопок"""
@bot.message_handler(func=lambda msg: msg.text in start_buttons_labels)
def handle_start_button(message: types.Message):
    user_id = message.from_user.id
    task = message.text
    user_info = UserInfo(user_id=user_id, task=task)
    users_info[user_id] = user_info  # Добавляем пользователя в список, пока без описания задачи
    bot.send_message(message.chat.id, "Теперь дайте описание задачи (ограничения, предметная область и т. д.)")


"""Обработчик описания задачи. 
Если пользователь ещё не дал описание задачи, то обработчик берёт текст из сообщения и ставит его как описание"""
@bot.message_handler(func=lambda msg: users_info.get(msg.from_user.id) and users_info[msg.from_user.id].description is None)
def handle_task_description(message: types.Message):
    user_id = message.from_user.id
    task_description = message.text
    users_info[user_id].description = task_description
    bot.send_message(message.chat.id, "Заказ оформлен. Ждите решение через некоторое время.")


bot.polling(none_stop=True)
