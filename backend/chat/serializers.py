from rest_framework import serializers
from .models import ChatMessage

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'question', 'answer', 'department', 'timestamp', 'sources','confidence']
        read_only_fields = ['id', 'timestamp', 'sources' ,'confidence'] 