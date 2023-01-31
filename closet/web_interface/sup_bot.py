import requests

API_TOKEN = '6002346755:AAHwXwHE0Vfd9EKVxkHyZ3WceEtBarkfD9c'
admin_name = 412940515
default_message = "Sorry... I'm having a little technical problem"

ALERT_TEXT = '''
Тема: {}

Описание:
{}

Логи:
{}
'''


import asyncio
from aiogram import Bot

API_TOKEN = '6002346755:AAHwXwHE0Vfd9EKVxkHyZ3WceEtBarkfD9c'
admin_name = 412940515


async def send_message(message):
    operator = Bot(API_TOKEN)
    await operator.send_message(admin_name, message)


async def send_attachment(path):
    operator = Bot(API_TOKEN)
    attachment = open(path, 'rb')
    await operator.send_document(admin_name, (path.split('/')[-1], attachment))


def send_support_message(theme=None, description=None, logs=None, attachment=None):
    if theme is None and description is None:
        message = default_message
    else:
        message = ALERT_TEXT.format(theme, description, logs)
    asyncio.run(send_message(message))
    # Если все ок, отправляем еще и вложения
    if attachment is not None and attachment != "":
        asyncio.run(send_attachment(str(attachment)))

    return 200
