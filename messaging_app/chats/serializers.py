from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "user_id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "created_at",
        ]


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.username", read_only=True)

    class Meta:
        model = Message
        fields = [
            "message_id",
            "sender_name",
            "conversation",
            "message_body",
            "sent_at",
        ]

    def validate_message_body(self, value):
        """Ensure message is not empty"""
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty")
        return value

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            "participants",
            "created_at",
            "messages",
        ]

    def get_messages(self, obj):
        """Return serialized messages for a conversation"""
        messages = obj.messages.all().order_by("-sent_at")
        return MessageSerializer(messages, many=True).data