import logging
import time

import requests
import telegram
from environs import Env

logger = logging.getLogger('bot_logger')


class LogsHandler(logging.Handler):

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)

    def __init__(self, tg_token, chat_id):
        logging.Handler.__init__(self)
        self.chat_id = chat_id
        self.bot = telegram.Bot(tg_token)


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
    tg_loger_token = env.str('TELEGRAM_LOGGER_TOKEN')
    chat_id = env('TG_CHAT_ID')

    logger.setLevel(logging.INFO)
    logger.addHandler(LogsHandler(tg_loger_token, chat_id))
    logger.info('Бот запущен')

    headers = {
        'Authorization': env('DEVMAN_TOKEN')
    }
    params = {}
    while True:
        try:
            response = requests.get('https://dvmn.org/api/long_polling/', headers=headers, params=params)
            response.raise_for_status()
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
        except requests.exceptions.ConnectionError:
            time.sleep(10)
        except requests.exceptions.ReadTimeout:
            continue
        except Exception as err:
            logger.exception(err)
