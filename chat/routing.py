from django.conf.urls import url
from .consumers import (ChatConsumer, AsyncChatConsumer, BaseSyncConsumer, BaseAsyncConsumer,
                        ChatJsonConsumer, ChatAsyncJsonConsumer)


websocket_urls = [
    url(r'^ws/chat/$', ChatAsyncJsonConsumer.as_asgi()),
    url(r'^ws/chat/(?P<room_name>\w+)/$', AsyncChatConsumer.as_asgi()),
]
