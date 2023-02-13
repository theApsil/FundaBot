from telebot import types, TeleBot
from sensitive_data import admin_ids
import task_database

"""Содержит хэндлеры и вспомогательный функционал для админки"""


ADMIN_COMMANDS = [
    "/admin - вывод общих сведений админской панели",
    "/tasks - получение всех существующих заданий",
    "/unfinished - получение всех невыполненных заданий",
    "/finish task_id - пометить задание task_id выполненным и (TODO) отправить пользователю сообщение о выполнении"
]


def main(bot: TeleBot):
    """Декоратор на проверку пользователя на админа"""
    def check_admin(func):
        def wrapper(message: types.Message, *args, **kwargs):
            user_id = message.from_user.id
            if user_id in admin_ids:
                return func(message, *args, **kwargs)
            else:
                bot.send_message(message.chat.id, "Ухади, ты не админ😠")
        return wrapper


    """/admin - вывод общих сведений админской панели"""
    @bot.message_handler(commands=["admin"])
    @check_admin
    def admin_menu(message: types.Message):
        bot.send_message(message.chat.id, "Добро пожаловать, господин.\nВот доступные на данный момент команды:")
        for comm in ADMIN_COMMANDS:
            bot.send_message(message.chat.id, comm)


    """/tasks - получение всех существующих заданий"""
    @bot.message_handler(commands=["tasks"])
    @check_admin
    def all_tasks(message: types.Message):
        bot.send_message(message.chat.id, "Все задания:")
        tasks_str = ""
        tasks = task_database.get_all_tasks()
        for task in tasks:
            tasks_str += str(task) + "\n"
        if len(tasks_str) == 0:
            tasks_str = "Заданий нет"
        bot.send_message(message.chat.id, tasks_str)
    

    """/unfinished - получение всех невыполненных заданий"""
    @bot.message_handler(commands=["unfinished"])
    @check_admin
    def unfinished_tasks(message: types.Message):
        bot.send_message(message.chat.id, "Все незавершённые задания:")
        tasks_str = ""
        tasks = task_database.get_uncompleted_tasks()
        for task in tasks:
            tasks_str += str(task) + "\n"
        if len(tasks_str) == 0:
            tasks_str = "Заданий нет"
        bot.send_message(message.chat.id, tasks_str)
    

    """/finish task_id - пометить задание task_id выполненным и (TODO) отправить пользователю сообщение о выполнении"""
    @bot.message_handler(commands=["finish"])
    @check_admin
    def finish(message: types.Message):
        bot.send_message(message.chat.id, "Пока не реализовано")
        # task_database.mark_task_completed(task_id)
        # bot.send_message(message.chat.id, f"Задание №{task_id} помечено выполненным")
