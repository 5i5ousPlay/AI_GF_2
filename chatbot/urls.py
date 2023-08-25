from django.urls import path
from .views import chatbot, ChatListView, CustomLoginView, CustomRegistrationView

urlpatterns = [
    path('', chatbot, name='chatbot'),
    path('list/', ChatListView.as_view(), name='chat-list'),
    path('login/', CustomLoginView.as_view(), name='chat-login'),
    path('register/', CustomRegistrationView.as_view(), name='chat-register'),
]

app_name = 'chatbot'
