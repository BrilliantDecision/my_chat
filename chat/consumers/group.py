from channels.db import database_sync_to_async
from .base import BaseChatConsumer


class ChatConsumer(BaseChatConsumer):
    async def event_chat_list(self, event):
        pass

    @database_sync_to_async
    def get_chat_list(self, user):
        pass


