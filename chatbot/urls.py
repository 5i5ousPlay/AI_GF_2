from django.urls import path
from .views import chatbot, ChatListView, CustomLoginView

urlpatterns = [
    path('', chatbot, name='chatbot'),
    path('list/', ChatListView.as_view(), name='chat-list'),
    path('login/', CustomLoginView.as_view(), name='chat-login')
]

app_name = 'chatbot'
