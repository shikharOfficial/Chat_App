from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse
from .serializers import ChatSerializer
from user.serializers import UserSerializer
from .models import Chats
from user.models import TblUser

class ChatsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        success = False
        data = None
        message = ''
        response_status = status.HTTP_500_INTERNAL_SERVER_ERROR

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
        response_status = 500
        success = False

        try:
            sender_id = request.user.id
            recipient_id = request.data.get("recipient")

            if sender_id == recipient_id:
                return JsonResponse({"error": "Sender cannot be the same as recipient."}, status=400)

            request.data['sender'] = sender_id

            chat_serializer = ChatSerializer(data=request.data)

            if chat_serializer.is_valid():
                chat_instance = chat_serializer.save()
                data = model_to_dict(chat_instance)
                success = True
                message = "Message Sent Successfully"
                response_status = 201

            else:
                message = chat_serializer.errors
                response_status = 400
                
        except Exception as e: 
            message = str(e)
        
        return JsonResponse({"success": success, "message": message, "data": data}, status=response_status)
    

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

            query = {
                recipient['recipient__id']: {
                    "id": recipient['recipient__id'],
                    "full_name": recipient['recipient__first_name'] + ' ' + recipient['recipient__last_name'],
                    "email": recipient['recipient__email']
                } 
                for recipient in Chats.objects.filter(sender_id=user_id).values("recipient__id", "recipient__first_name", "recipient__last_name", "recipient__email").distinct()
            }

            users_already_messaged = query.values()

            users_already_messaged_ids = query.keys()

            new_users = TblUser.objects.exclude(id=user_id).exclude(id__in=users_already_messaged_ids) 

            serialized_new_users = UserSerializer(instance=new_users, many = True)

            formatted_serialized_new_users = [{ "id": userDetail["id"], "full_name": userDetail["first_name"] + userDetail["last_name"], "email": userDetail["email"] } for userDetail in serialized_new_users.data]
            
            data = {
                "users_already_messaged": users_already_messaged,
                "new_users": formatted_serialized_new_users
            }
            success = True
            message = "Users fetched Successfully"
            resposne_status = status.HTTP_200_OK

        except Exception as e:
            message = str(e) 

        return Response({ "success": success, "message": message, "data": data}, status=resposne_status)


def chat_page_redirect(request, recipient_id):
    return render(request, 'chatPage.html', {"recipient_id":recipient_id})

