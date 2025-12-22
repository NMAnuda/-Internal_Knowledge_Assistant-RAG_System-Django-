from rest_framework import serializers
from .models import ChatMessage

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'question', 'answer', 'department', 'timestamp', 'sources']
        read_only_fields = ['id', 'timestamp', 'sources']  # User can't edit these