from django.urls import path
from .views import ChatsView

urlpatterns = [
    path('chats-from-user/', ChatsView.as_view(), name="chats_from_a_user"),
]