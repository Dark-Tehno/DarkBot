import logging


class Dispatcher:
    """
    Направляет обновления зарегистрированным обработчикам.
    """
    def __init__(self, bot):
        self.bot = bot
        self.handlers = []
        self.logger = logging.getLogger(self.__class__.__name__)

    def add_handler(self, handler):
        self.handlers.append(handler)

    def process_update(self, update):
        for handler in self.handlers:
            if handler.check_update(update):
                try:
                    handler.handle_update(update, self)
                except Exception:
                    self.logger.exception("Ошибка в обработчике %s", handler.__class__.__name__)
                break  # Останавливаемся после первого совпавшего обработчика