from typing import List, Union


class Handler:
    """Базовый класс для всех обработчиков."""
    def __init__(self, callback):
        if not callable(callback):
            raise TypeError("Callback должен быть вызываемой функцией.")
        self.callback = callback

    def check_update(self, update) -> bool:
        """Возвращает True, если обновление должно быть обработано этим обработчиком."""
        raise NotImplementedError

    def handle_update(self, update, dispatcher):
        """Выполняет callback для обновления."""
        self.callback(update)


class CommandHandler(Handler):
    """Обрабатывает команду, например /start."""
    def __init__(self, command: Union[str, List[str]], callback):
        super().__init__(callback)
        if isinstance(command, str):
            self.commands = [command.lower()]
        else:
            self.commands = [c.lower() for c in command]

    def check_update(self, update) -> bool:
        return (update.message and update.message.text and
                update.message.text.startswith('/') and
                update.message.text.split(maxsplit=1)[0][1:].lower() in self.commands)


class Filters:
    """Простые фильтры для сообщений."""
    TEXT = 1
    PHOTO = 2


class MessageHandler(Handler):
    """Обрабатывает обычное текстовое сообщение."""
    def __init__(self, filters, callback):
        super().__init__(callback)
        self.filters = filters

    def check_update(self, update) -> bool:
        if not update.message:
            return False

        if self.filters == Filters.TEXT:
            return bool(update.message.text)
        if self.filters == Filters.PHOTO:
            return bool(update.message.photo)

        # По умолчанию (filters=None) соответствует любому текстовому сообщению, не являющемуся командой
        return bool(update.message and update.message.text)