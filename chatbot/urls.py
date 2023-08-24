from django.urls import path
from .views import chatbot, ChatListView

urlpatterns = [
    path('', chatbot, name='chatbot'),
    path('list/', ChatListView.as_view(), name='chat-list'),
]
