from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()  # Uses your custom User from accounts

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_history')
    question = models.TextField()
    answer = models.TextField()
    department = models.CharField(max_length=100, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    sources = models.JSONField(default=list, blank=True)
    confidence = models.CharField(max_length=10, default='medium', choices=[  # 🔥 NEW FIELD
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low')
    ])

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.question[:50]}..."