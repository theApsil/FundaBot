import telebot
from dataclasses import dataclass
from telebot import types
from sensitive_data import telegram_token
from enum import Enum
import task_database
import admin_handlers


bot = telebot.TeleBot(telegram_token)

class UserStatus(Enum):
    STARTED = 0  # Только создан, ещё не производил никаких операций
    CHOOSING_TASK = 1  # В процессе выбора задания
    GIVING_DESCRIPTION = 2  # Даёт описание к выбранному заданию
    CHOOSING_COURSEWORK_TYPE = 3  # Выбирает между услугами курсовой работы
    BEETWEEN_CHOOSING_COURSEWORK_TYPE_AND_GIVING_DESCRIPTION = 4  # Либо выбирает другой тип курсовой работы, либо пишет описание задачи
    FINISHED = 5  # Закончил оформление заказа


@dataclass
class UserInfo:
    user_id: int
    status: UserStatus
    task: str = None  # Задание (номер лабы или курсач)
    description: str = None  # Описание задания (всякие ограничения и предметная область)



# Сюда будут добавляться пользователи, совершившие заказ
users_info: dict[int, UserInfo] = dict()  # user_id : UserInfo

START_BUTTONS = [
    "2.1 (Поиск в строке)",
    "2.2 (Поиск в массиве)",
    "2.3 (Хеш-Таблицы)",
    "2.4 (Графы)",
    "Курсовая работа",
]

COURSE_WORK_BUTTONS = [
    "Программа",
    "Программа + Отчёт"
]


def create_user(message: types.Message):
    user_id = message.from_user.id
    users_info[user_id] = UserInfo(user_id, UserStatus.STARTED)

def set_user_status(message: types.Message, status: UserStatus):
    user_id = message.from_user.id
    users_info[user_id].status = status


def get_user_status(message) -> UserStatus:
    user_id = message.from_user.id
    return users_info[user_id].status


# Создаём админские хендлеры
admin_handlers.main(bot)


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

    # Создаём панель стартовых кнопок
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    btns = []
    for btn_label in START_BUTTONS:
        btn = types.KeyboardButton(text=btn_label)
        btns.append(btn)
    markup.add(*btns)

    bot.send_message(message.chat.id, "Выберите нужную функцию:", reply_markup=markup)
    create_user(message)
    set_user_status(message, UserStatus.CHOOSING_TASK)


"""/help"""
@bot.message_handler(commands=['help'])
def help(message: types.Message):
    bot.send_message(message.chat.id, "Временно недоступно")


"""/get_users - возвращает users_info для дебага"""
@bot.message_handler(commands=["get_users"])  # TODO: Убрать, либо перенести в админку
def get_users(message: types.Message):
    bot.send_message(message.chat.id, str(users_info))


"""Обработчик всех стартовых кнопок"""
@bot.message_handler(func=lambda msg: 
                     get_user_status(msg) == UserStatus.CHOOSING_TASK
                     and msg.text in START_BUTTONS)
def handle_start_button(message: types.Message):

    # Запоминаем задание, выбранное пользователем
    user_id = message.from_user.id
    task = message.text
    users_info[user_id].task = task

    if task == "Курсовая работа":
        # Создаём панель с кнопками для выбора типа курсовой работы
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        btns = []
        for btn_label in COURSE_WORK_BUTTONS:
            btn = types.KeyboardButton(text=btn_label)
            btns.append(btn)
        markup.add(*btns)

        sMess = f'<b>Курсовая работа - самая объёмная и сложная работа на всём твоём 2м курсе</b>\nНа нашем потоке её закрыло только <b><i>16</i></b> человек из <b><i>96</i></b>'
        bot.send_message(message.chat.id, sMess, parse_mode='html')
        bot.send_message(message.chat.id, "Что ты хочешь заказать?", reply_markup=markup)
        set_user_status(message, UserStatus.CHOOSING_COURSEWORK_TYPE)
    else:  # Выбрали какую-либо лабу
        bot.send_message(message.chat.id, "Теперь дайте описание задачи (ограничения, предметная область и т. д.)")
        set_user_status(message, UserStatus.GIVING_DESCRIPTION)
    


"""Обработчик кнопок курсовой работы"""
@bot.message_handler(func=lambda message: 
                     (get_user_status(message) == UserStatus.CHOOSING_COURSEWORK_TYPE 
                      or get_user_status(message) == UserStatus.BEETWEEN_CHOOSING_COURSEWORK_TYPE_AND_GIVING_DESCRIPTION)
                     and message.text in COURSE_WORK_BUTTONS)
def handle_coursework_button(message: types.Message):

    # Запоминаем тип курсовой работы пользователя
    course_work_type = message.text
    user_id = message.from_user.id
    users_info[user_id].task = f"Курсовая работа ({course_work_type})"

    if message.text == "Программа":
        sMess = f'<b>{message.from_user.first_name}</b>, помни что  <b>Крестникова</b> - любит дрочить за отчёты, ещё не поздно изменить выбор'
        bot.send_message(message.chat.id, sMess, parse_mode='html')
        bot.send_message(message.chat.id,
                         "Если ты уверен в своём выборе, то опиши мне <b>справочники и базовую спецификацию</b>\nИли измени свой выбор нажав на кнопку <b><i>Программа + Отчёт</i></b>",
                         parse_mode='html')
        set_user_status(message, UserStatus.BEETWEEN_CHOOSING_COURSEWORK_TYPE_AND_GIVING_DESCRIPTION)
    elif message.text == "Программа + Отчёт":
        sMess = f'Молодец, <b>{message.from_user.first_name}</b>, ты сделал правильный выбор'
        bot.send_message(message.chat.id, sMess, parse_mode='html')
        bot.send_message(message.chat.id,
                         "Опиши мне <b>справочники и базовую спецификацию</b>",
                         parse_mode='html')
        set_user_status(message, UserStatus.GIVING_DESCRIPTION)


"""Обработчик описания задачи. 
Если пользователь ещё не дал описание задачи, то обработчик берёт текст из сообщения и ставит его как описание"""
@bot.message_handler(func=lambda msg: 
                     get_user_status(msg) == UserStatus.GIVING_DESCRIPTION
                     or (msg.text not in COURSE_WORK_BUTTONS and get_user_status(msg) == UserStatus.BEETWEEN_CHOOSING_COURSEWORK_TYPE_AND_GIVING_DESCRIPTION))
def handle_task_description(message: types.Message):
    user_id = message.from_user.id
    task_description = message.text
    users_info[user_id].description = task_description
    bot.send_message(message.chat.id, "Заказ оформлен. Ждите решение через некоторое время.")
    bot.send_message(message.chat.id, "Если хотите оформить ещё один заказ, пропишите /start.")
    set_user_status(message, UserStatus.FINISHED)
    
    # Заказ оформлен. Добавляем его в базу данных
    user_info = users_info[user_id]
    task_database.create_task(user_id, user_info.task, user_info.description)


"""Обработчик всех остальных случаев, не подходящих под предыдущие"""
@bot.message_handler()
def handle_other_cases(message: types.Message):
    bot.send_message(message.chat.id, "Да-да, очень интересно. Может будешь писать то, чего от тебя просят?")

bot.polling(none_stop=True)
