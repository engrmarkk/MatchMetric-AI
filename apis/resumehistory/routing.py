from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/resume-tailor/$", consumers.ResumeConsumer.as_asgi()),
]
