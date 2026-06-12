from django.urls import path

from .push_views import SendPushView
from .views import DeviceTokenRegisterView, PushNotificationListView

urlpatterns = [
    path("register/", DeviceTokenRegisterView.as_view()),
    path("history/", PushNotificationListView.as_view()),
    path("send/", SendPushView.as_view()),
]
