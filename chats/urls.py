from django.urls import path
from .views import ChatsView, UsersFromChats, chat_page_redirect

urlpatterns = [
    path('chats-from-user/', ChatsView.as_view(), name="chats_from_a_user"),
    path('user/', UsersFromChats.as_view(), name="user__for_chats"), 
    path('chat-page/<int:recipient_id>', chat_page_redirect, name="chat_page")
]