from rest_framework import generics, permissions

from .models import DeviceToken, PushNotification
from .serializers import DeviceTokenSerializer, PushNotificationSerializer


class DeviceTokenRegisterView(generics.CreateAPIView):
    serializer_class = DeviceTokenSerializer
    permission_classes = [permissions.IsAuthenticated]


class PushNotificationListView(generics.ListAPIView):
    serializer_class = PushNotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PushNotification.objects.filter(user=self.request.user)[:50]
