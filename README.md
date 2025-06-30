# DarkBot

Клиентская библиотека Python для взаимодействия с DarkBot.

## Установка
Для установки последней версии напрямую с GitHub:
```bash
pip install git+https://github.com/Dark-Tehno/DarkBot.git
```

## Использование

```python
import os
import logging

from DarkBot.v2.bot import Bot
from DarkBot.v2.updater import Updater
from DarkBot.v2.handlers import CommandHandler, MessageHandler
from DarkBot.v2.types import Update

BOT_TOKEN = 'ВАШ ТОКЕН ПОЛУЧЕНЫЙ ИЗ https://vsp210.ru/chat/1_bot/'  

# Настройка логирования для более информативного вывода
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# --- Функции-обработчики ---

def start(update: Update):
    """Обработчик для команды /start."""
    message = update.message
    logging.info("Получена команда /start в чате %d", message.chat.id)
    message.reply_text('Привет! Я эхо-бот, созданный с помощью библиотеки DarkBot.')


def echo(update: Update):
    """Обработчик, который повторяет все текстовые сообщения."""
    message = update.message
    logging.info("Эхо сообщения в чат %d: '%s'", message.chat.id, message.text)
    message.reply_text(message.text)


def main():
    """Основная функция для запуска бота."""
    bot = Bot(token=BOT_TOKEN)
    updater = Updater(bot)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(filters=None, callback=echo))

    updater.start_polling()


if __name__ == '__main__':
    if os.name == 'nt':
        os.system('chcp 65001 > nul')
    main()
```