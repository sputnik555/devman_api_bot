## Бот уведомлений о проверке работ
Бот предназначен для отправки в Telegram уведомлений о проверке работ на сайте https://dvmn.org/

### Переменные окружения
Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` и
запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

Доступны 3 переменные:
- `DEVMAN_TOKEN` — Токен API Devman ([документация](https://dvmn.org/api/docs/)).
- `TELEGRAM_TOKEN` — Токен бота для отправки уведомлений
- `TELEGRAM_LOGGER_TOKEN` - Токен бота для логирования
- `TG_CHAT_ID` - ID чата, в который будут отправляться сообщения. Можно получить у бота `@userinfobot`

### Запуск бота
Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, если есть конфликт с Python2) для установки зависимостей:
```bash
pip install -r requirements.txt
```

Для запуска скрипта необходимо выполнить в консоли команду:

```bash
python main.py
```

### Запуск бота в Docker
1. Собираем образ
```bash
docker build -t tg_bot:latest .
```
2. Запускаем контейнер
```bash
docker run --env-file ./.env tg_bot
```