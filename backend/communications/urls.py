from django.urls import path

from .views import RadioBroadcastView, SendSMSView, USSDWebhookView, VoiceCallView, VoiceMessageView

urlpatterns = [
    path("sms/send/", SendSMSView.as_view()),
    path("ussd/", USSDWebhookView.as_view()),
    path("voice/", VoiceMessageView.as_view()),
    path("voice/call/", VoiceCallView.as_view()),
    path("radio/broadcast/", RadioBroadcastView.as_view()),
]
