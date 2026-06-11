from django.urls import path

from .views import DeviceTokenRegisterView, PushNotificationListView

urlpatterns = [
    path("register/", DeviceTokenRegisterView.as_view()),
    path("history/", PushNotificationListView.as_view()),
]
