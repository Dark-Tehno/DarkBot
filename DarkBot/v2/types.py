import io

class User:
    """Представляет пользователя."""
    def __init__(self, username: str):
        self.username = username

    @classmethod
    def from_dict(cls, data: dict):
        if not data:
            return cls(username='Неизвестный пользователь')
        return cls(username=data.get('username', 'Неизвестный пользователь'))

    def __repr__(self):
        return f"User(username='{self.username}')"


class Chat:
    """Представляет чат."""
    def __init__(self, id: int):
        self.id = id

    def __repr__(self):
        return f"Chat(id={self.id})"


class PhotoSize:
    """Представляет один размер фото."""
    def __init__(self, file_id: str, width: int, height: int, file_size: int = None, bot=None):
        self.file_id = file_id
        self.width = width
        self.height = height
        self.file_size = file_size
        self._bot = bot

    @classmethod
    def from_dict(cls, data: dict, bot=None):
        if not data:
            return None
        return cls(
            file_id=data['file_id'],
            width=data['width'],
            height=data['height'],
            file_size=data.get('file_size'),
            bot=bot
        )

    def download(self, out_stream: io.BytesIO):
        """Удобный метод для загрузки этого размера фото."""
        if not self._bot:
            raise RuntimeError("Объект PhotoSize не привязан к экземпляру Bot.")
        file_info = self._bot.get_file(self.file_id)
        return self._bot.download_file(file_info['file_path'], out_stream)

    def __repr__(self):
        return f"PhotoSize(file_id='{self.file_id}', width={self.width}, height={self.height})"


class Message:
    """Представляет сообщение."""
    def __init__(self, message_id: int, chat: 'Chat', from_user: 'User', text: str, date: str, photo: list = None, bot=None):
        self.message_id = message_id
        self.chat = chat
        self.from_user = from_user
        self.text = text
        self.date = date
        self.photo = photo or []
        self._bot = bot

    @classmethod
    def from_dict(cls, data: dict, bot=None):
        if not data:
            return None
        
        chat = Chat(id=data['chat_room_id'])
        user = User.from_dict(data.get('user', {}))

        photo_data = data.get('photo')
        photos = []
        if photo_data:
            # Сортируем фото от большего к меньшему, чтобы легко брать лучшее качество
            photos = sorted(
                [PhotoSize.from_dict(p, bot=bot) for p in photo_data if p],
                key=lambda p: (p.width * p.height),
                reverse=True
            )

        return cls(
            message_id=data['id'],
            chat=chat,
            from_user=user,
            text=data.get('text'),
            photo=photos,
            date=data.get('created_at'),
            bot=bot
        )

    def reply_text(self, text: str):
        """Удобный метод для ответа на это сообщение."""
        if not self._bot:
            raise RuntimeError("Объект сообщения не привязан к экземпляру Bot.")
        return self._bot.send_message(chat_id=self.chat.id, text=text)

    def __repr__(self):
        return f"Message(id={self.message_id}, from='{self.from_user.username}', text='{self.text[:20]}...')"


class Update:
    """Представляет входящее обновление от API."""
    def __init__(self, update_id: int, message: 'Message'):
        self.update_id = update_id
        self.message = message

    @classmethod
    def from_dict(cls, data: dict, bot=None):
        """
        Пользовательский API возвращает список сообщений, а не объектов 'update'.
        Мы будем рассматривать каждое сообщение как новое обновление, используя его ID в качестве update_id.
        """
        message = Message.from_dict(data, bot=bot)
        if not message:
            return None
        return cls(update_id=message.message_id, message=message)

    def __repr__(self):
        return f"Update(id={self.update_id}, message={self.message})"