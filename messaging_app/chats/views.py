from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for conversations.
    - List conversations
    - Create a new conversation
    - Retrieve a single conversation with messages
    """

    queryset = Conversation.objects.all().prefetch_related("participants", "messages")
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with participants.
        Expects a list of participant user_ids.
        """
        participant_ids = request.data.get("participants", [])
        if not participant_ids:
            return Response(
                {"error": "At least one participant is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        participants = User.objects.filter(user_id__in=participant_ids)
        if not participants.exists():
            return Response(
                {"error": "No valid participants found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for messages.
    - List messages
    - Send a message in a conversation
    """

    queryset = Message.objects.all().select_related("sender", "conversation")
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        """
        Send a message to an existing conversation.
        Expects: sender (user_id), conversation (conversation_id), message_body
        """
        sender_id = request.data.get("sender")
        conversation_id = request.data.get("conversation")
        message_body = request.data.get("message_body")

        if not (sender_id and conversation_id and message_body):
            return Response(
                {"error": "sender, conversation, and message_body are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            sender = User.objects.get(user_id=sender_id)
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid sender user_id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Invalid conversation_id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        message = Message.objects.create(
            sender=sender, conversation=conversation, message_body=message_body
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

