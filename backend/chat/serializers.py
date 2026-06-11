from rest_framework import serializers

from .models import ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.get_full_name", read_only=True)
    sender_role = serializers.CharField(source="sender.role", read_only=True)

    class Meta:
        model = ChatMessage
        fields = [
            "id", "incident", "sender", "sender_name", "sender_role",
            "message", "attachment", "is_read", "created_at",
        ]
        read_only_fields = ["id", "sender", "created_at"]

    def create(self, validated_data):
        validated_data["sender"] = self.context["request"].user
        return super().create(validated_data)
