from django.conf.urls import url


websocket_urls = [
    url(r'^ws/chat/$', ChatAsyncJsonConsumer.as_asgi()),
    url(r'^ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
]
