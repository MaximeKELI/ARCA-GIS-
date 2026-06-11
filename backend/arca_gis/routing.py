from django.urls import path

from alerts.consumers import AlertConsumer
from chat.consumers import ChatConsumer
from users.consumers import GPSTrackingConsumer

websocket_urlpatterns = [
    path("ws/alerts/", AlertConsumer.as_asgi()),
    path("ws/gps/", GPSTrackingConsumer.as_asgi()),
    path("ws/chat/<int:incident_id>/", ChatConsumer.as_asgi()),
]
