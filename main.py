import time

import requests
import telegram
from environs import Env


def send_message(tg_token, chat_id, is_negative, lesson_title, lesson_url):
    bot = telegram.Bot(tg_token)
    if is_negative:
        result_text = 'К сожалению в работе нашлись ошибки'
    else:
        result_text = 'Преподавателю всё понравилось, можно приступать к следующему уроку'
    message_text = 'У вас проверили работу 	«{}»\n\n{}\n\n{}'\
        .format(lesson_title, result_text, lesson_url)
    bot.send_message(chat_id=chat_id, text=message_text)


if __name__ == '__main__':
    env = Env()
    env.read_env()
    tg_token = env.str('TELEGRAM_TOKEN')
    chat_id = env('TG_CHAT_ID')
    headers = {
        'Authorization': env('DEVMAN_TOKEN')
    }
    params = {}
    while True:
        try:
            response = requests.get('https://dvmn.org/api/long_polling/', headers=headers, params=params)
            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            time.sleep(10)
            continue
        except requests.exceptions.ReadTimeout:
            continue
        attempt_statuses = response.json()
        if attempt_statuses.get('status') == 'found':
            params['timestamp'] = attempt_statuses.get('last_attempt_timestamp')
            for attempt in attempt_statuses.get('new_attempts'):
                send_message(
                  tg_token,
                  chat_id,
                  attempt.get('is_negative'),
                  attempt.get('lesson_title'),
                  attempt.get('lesson_url')
                )
        elif attempt_statuses.get('status') == 'timeout':
            params['timestamp'] = attempt_statuses.get('timestamp_to_request')
          