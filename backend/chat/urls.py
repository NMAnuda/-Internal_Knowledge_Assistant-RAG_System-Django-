from django.urls import path
from .views import AskQuestionView , ChatHistoryView, OllamaHealthCheck

urlpatterns = [
    path('ask/', AskQuestionView.as_view(), name='ask_question'),
    path('history/', ChatHistoryView, name='history'),
    path('health/', OllamaHealthCheck, name='ollama_health'),
]
