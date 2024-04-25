from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Chats
from .serializers import ChatSerializer
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.db.models import Q


class ChatsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        success = False
        data = None
        message = ''
        response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        user_id = None

        try:
            receiver = request.GET.get('receiver')
            sender = request.user.id

            chats = Chats.objects.filter(Q(sender_id=sender, recipient_id=receiver) | Q(sender_id=receiver, recipient_id=sender)).order_by("sent_at")

            chats_serializer = ChatSerializer(chats, many = True)
            data = chats_serializer.data
            success = True
            message = "Chats received successfully"
            response_status = status.HTTP_200_OK
        except Exception as e: 
            message = str(e)

        return Response({ "success": success, "message": message, "data": data, "user_id": sender }, status=response_status)
    
    def post(self, request):
        data = None
        message = ''
        resposne_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        success = False

        try:
            sender_id = request.user.id
            recipient_id = request.data.get("recipient")

            if sender_id == recipient_id:
                return Response({"error": "Sender cannot be the same as recipient."}, status=status.HTTP_400_BAD_REQUEST)

            request.data['sender'] = sender_id

            chat_serializer = ChatSerializer(data=request.data)

            if chat_serializer.is_valid():
                chat_instance = chat_serializer.save()
                data = model_to_dict(chat_instance)
                success = True
                message = "Message Sent Successfully"
                resposne_status = status.HTTP_201_CREATED
            else:
                message = chat_serializer.errors
                resposne_status = status.HTTP_400_BAD_REQUEST
                
        except Exception as e: 
            message = str(e)
    
        return Response({ "success": success, "message": message, "data": data}, status=resposne_status)
    

class UsersFromChats(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = None
        message = ''
        resposne_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        success = False

        try:
            user_id = request.user.id

            recipient_info = {
                recipient['recipient__id']: {
                    "id": recipient['recipient__id'],
                    "full_name": recipient['recipient__first_name'] + ' ' + recipient['recipient__last_name'],
                    "email": recipient['recipient__email']
                } 
                for recipient in Chats.objects.filter(sender_id=user_id).values("recipient__id", "recipient__first_name", "recipient__last_name", "recipient__email").distinct()
            }.values()

            data = recipient_info
            success = True
            message = "Users fetched Successfully"
            resposne_status = status.HTTP_200_OK

        except Exception as e:
            message = str(e) 

        return Response({ "success": success, "message": message, "data": data}, status=resposne_status)


def chat_page_redirect(request, recipient_id):
    return render(request, 'chatPage.html', {"recipient_id":recipient_id})

