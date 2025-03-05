from django.urls import re_path
from .consumers import MonitoringConsumer

websocket_urlpatterns = [
    re_path(r"ws/monitoring/$", MonitoringConsumer.as_asgi()),
]
