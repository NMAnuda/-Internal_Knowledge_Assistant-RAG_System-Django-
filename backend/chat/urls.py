from django.urls import path
from .views import AskQuestionView , ChatHistoryView

urlpatterns = [
    path('ask/', AskQuestionView.as_view(), name='ask_question'),
    path('history/', ChatHistoryView, name='history'),
]
