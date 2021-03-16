from django.conf.urls import url
from .consumers import (ChatConsumer, AsyncChatConsumer, BaseSyncConsumer, BaseAsyncConsumer,
                        ChatJsonConsumer, ChatAsyncJsonConsumer)


websocket_urls = [
    url(r'^ws/chat/$', ChatConsumer.as_asgi()),
]
