import time
import logging
from .bot import Bot
from .dispatcher import Dispatcher
from .exceptions import ApiError, NetworkError


class Updater:
    """
    Этот класс непрерывно опрашивает сервер на наличие обновлений и передает их в Dispatcher.
    """
    def __init__(self, bot: Bot):
        self.bot = bot
        self.dispatcher = Dispatcher(bot)
        self._last_update_id = 0
        self._is_running = False
        self.logger = logging.getLogger(self.__class__.__name__)

    def _get_initial_last_message_id(self) -> int:
        """
        Получает ID последнего сообщения при запуске, чтобы избежать обработки старых сообщений.
        """
        self.logger.info("Получение ID последнего сообщения для пропуска старых...")
        try:
            updates = self.bot.get_updates(offset=0, timeout=5)
            if updates:
                last_id = updates[-1].update_id
                self.logger.info("Успешно. Бот будет обрабатывать сообщения после ID %d.", last_id)
                return last_id
            else:
                self.logger.info("Существующие сообщения не найдены. Начинаем с 0.")
        except (ApiError, NetworkError) as e:
            self.logger.warning("Не удалось получить начальный ID сообщения: %s. Начинаем с 0.", e)
        return 0

    def start_polling(self, poll_interval: float = 0.0, timeout: int = 25):
        """Запускает цикл long polling."""
        self._is_running = True
        self._last_update_id = self._get_initial_last_message_id()
        
        self.logger.info("Бот запущен в режиме long polling. Нажмите Ctrl+C для остановки.")
        
        while self._is_running:
            try:
                updates = self.bot.get_updates(offset=self._last_update_id, timeout=timeout)
                if updates:
                    for update in updates:
                        self.dispatcher.process_update(update)
                    self._last_update_id = updates[-1].update_id
                time.sleep(poll_interval)
            except KeyboardInterrupt:
                self.stop()
            except (ApiError, NetworkError) as e:
                self.logger.error("Ошибка в цикле опроса: %s. Повторная попытка через 5 секунд...", e)
                time.sleep(5)
            except Exception:
                self.logger.exception("Непредвиденная ошибка в цикле опроса. Повторная попытка через 10 секунд...")
                time.sleep(10)

    def stop(self):
        """Останавливает цикл опроса."""
        if self._is_running:
            self.logger.info("Остановка бота...")
            self._is_running = False