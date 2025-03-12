from django.urls import re_path
from sofia_blog.consumers import ArticleConsumer


websocket_urlpatterns = [
    re_path(r"ws/articles/$", ArticleConsumer.as_asgi()),
]
