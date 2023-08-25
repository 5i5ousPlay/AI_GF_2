import openai
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from .models import Chat
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from dj_rest_auth.views import LoginView
from dj_rest_auth.registration.views import RegisterView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, reverse
from .serializers import ChatSerializer

# Create your views here.

openai.api_key = settings.OPENAI_API_KEY


def ask_openai(message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a loving girlfriend that speaks in an UwU voice. MAKE SURE YOU ALWAYS SPEAK IN AN UWU VOICE."},
            {"role": "user", "content": message},
        ]
    )

    answer = response.choices[0].message.content.strip()
    return answer


@login_required()
def chatbot(request):
    chats = Chat.objects.filter(user=request.user)

    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)

        chat = Chat.objects.create(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html', {'chats': chats})


class ChatListView(generics.ListAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Chat.objects.filter(user=self.request.user)


class CustomLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data)
        self.serializer.is_valid(raise_exception=True)

        self.login()
        return redirect(reverse('chatbot:chatbot'))


class CustomRegistrationView(RegisterView):
    def post(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)
        return redirect(reverse('chatbot:chatbot'))
