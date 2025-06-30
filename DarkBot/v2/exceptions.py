class BotLibError(Exception):
    """Базовое исключение для этой библиотеки."""
    pass


class NetworkError(BotLibError):
    """Представляет сетевую ошибку во время вызова API."""
    def __init__(self, message, original_exception=None):
        super().__init__(message)
        self.original_exception = original_exception


class ApiError(BotLibError):
    """Представляет ошибку, возвращенную API (например, коды состояния 4xx или 5xx)."""
    def __init__(self, message, status_code=None, response_text=None):
        super().__init__(message)
        self.status_code = status_code
        self.response_text = response_text