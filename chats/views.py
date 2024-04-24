from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Chats
from .serializers import ChatSerializer

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

            chats = Chats.objects.filter(sender_id = sender, recipient_id = receiver).order_by("-sent_at")

            chats_serializer = ChatSerializer(chats, many = True)
            data = chats_serializer.data
            success = True
            message = "Chats received successfully"
            response_status = status.HTTP_200_OK
        except Exception as e: 
            message = str(e)

        return Response({ "success": success, "message": message, "data": data}, status=response_status)
    
    def post(self, request):
        pass

