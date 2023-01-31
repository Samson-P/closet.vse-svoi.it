import requests

API_TOKEN = '6002346755:AAHwXwHE0Vfd9EKVxkHyZ3WceEtBarkfD9c'
admin_name = 412940515
req_send_text = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'
req_send_doc = 'https://api.telegram.org/bot{}/sendDocument?chat_id={}'
default_message = "Sorry... I'm having a little technical problem"

ALERT_TEXT = '''
Тема: {}

Описание:
{}

Логи:
{}
'''


def send_support_message(theme=None, description=None, logs=None, attachment=None):
    if theme is None and description is None:
        message = default_message
    else:
        message = ALERT_TEXT.format(theme, description, logs)
    request = req_send_text.format(API_TOKEN, admin_name, message)
    response = requests.get(request)
    # Если все ок, отправляем еще и вложения
    if response.status_code == 200 and attachment is not None:
        print(attachment)
        request = req_send_doc.format(API_TOKEN, admin_name)
        files = {
            's.png': open(str(attachment), 'rb')
        }
        response = requests.post(request, files=files)
        print(response)
        # response = requests.get(request)

    return response
