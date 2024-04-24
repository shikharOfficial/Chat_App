from rest_framework import serializers
from .models import Chats

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chats
        fields = '__all__'
