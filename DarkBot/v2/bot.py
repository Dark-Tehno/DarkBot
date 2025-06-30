import requests
from typing import List, Optional
import io

from .types import Update
from .exceptions import NetworkError, ApiError


class Bot:
    """Основной класс для взаимодействия с API бота."""
    def __init__(self, token: str, base_url: str = 'https://vsp210.ru'):
        if not token:
            raise ValueError("Токен бота не может быть пустым.")
        self.token = token
        self.base_api_url = f'{base_url}/api/v2/bot'
        self._session = requests.Session()
        self._session.headers.update({'Authorization': f'Bot {self.token}'})

    def get_updates(self, offset: int = 0, timeout: int = 30) -> List[Update]:
        """
        Опрашивает сервер на наличие новых обновлений с использованием long polling.
        """
        url = f'{self.base_api_url}/updates/'
        params = {'last_message_id': offset}
        try:
            response = self._session.get(url, params=params, timeout=timeout)
            
            if response.status_code == 204:  # Нет новых сообщений
                return []
            
            response.raise_for_status()

            messages_data = response.json()
            updates = [Update.from_dict(msg_data, bot=self) for msg_data in messages_data]
            return updates

        except requests.exceptions.Timeout:
            return []  # Ожидаемое поведение при long polling, не ошибка.
        except requests.exceptions.HTTPError as e:
            raise ApiError(f"API вернуло ошибку: {e.response.status_code}",
                           status_code=e.response.status_code, response_text=e.response.text) from e
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Произошла сетевая ошибка: {e}", original_exception=e) from e

    def get_file(self, file_id: str) -> dict:
        """Получает информацию о файле по его ID."""
        url = f'{self.base_api_url}/get-file/{file_id}/'
        try:
            response = self._session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            raise ApiError(f"API вернуло ошибку при получении файла: {e.response.status_code}",
                           status_code=e.response.status_code, response_text=e.response.text) from e
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Произошла сетевая ошибка при получении файла: {e}", original_exception=e) from e

    def download_file(self, file_path: str, out_stream: io.BytesIO):
        """Загружает файл по его пути."""
        # base_url is like 'http://127.0.0.1:8000', file_path is like '/media/photos/...'
        # Мы извлекаем базовый URL (без /api/v2/bot) для скачивания медиафайла.
        base_download_url = self.base_api_url.rsplit('/api/', 1)[0]
        download_url = f"{base_download_url}{file_path}"
        try:
            with self._session.get(download_url, stream=True, timeout=30) as response:
                response.raise_for_status()
                for chunk in response.iter_content(chunk_size=8192):
                    out_stream.write(chunk)
        except requests.exceptions.HTTPError as e:
            raise ApiError(f"API вернуло ошибку при загрузке файла: {e.response.status_code}",
                           status_code=e.response.status_code, response_text=e.response.text) from e
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Произошла сетевая ошибка при загрузке файла: {e}", original_exception=e) from e

    def send_message(self, chat_id: int, text: str) -> Optional[dict]:
        """Отправляет текстовое сообщение в указанный чат."""
        url = f'{self.base_api_url}/send-message/'
        data = {'chat_id': chat_id, 'text': text}
        try:
            response = self._session.post(url, json=data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            raise ApiError(f"API вернуло ошибку при отправке сообщения: {e.response.status_code}",
                           status_code=e.response.status_code, response_text=e.response.text) from e
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Произошла сетевая ошибка при отправке сообщения: {e}", original_exception=e) from e