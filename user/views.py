from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from .serializers import UserSerializer, GetUserDetailsSerializer, LoginUserSerializer
from .models import TblUser
from rest_framework_simplejwt.tokens import RefreshToken 
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

class UserView(APIView):
    def post(self, request):
        success = False
        data = None
        message = ''
        responseCode = status.HTTP_500_INTERNAL_SERVER_ERROR
        try:
            payload = {
                "first_name": request.data.get("first_name"),
                "last_name": request.data.get("last_name"),
                "email": request.data.get("email"),
                "password": make_password(request.data.get("password")),
                "is_active": True,
                "is_deleted": False,
            }
            user_serializer = UserSerializer(data=payload)

            if user_serializer.is_valid():
                userInstance = user_serializer.save()
                success = True
                data = {"id": userInstance.id}
                message = "User Added"
                responseCode = status.HTTP_201_CREATED
            else:
                message = user_serializer.errors
                responseCode = status.HTTP_400_BAD_REQUEST

        except Exception as e: 
            message = str(e)
    
        return Response({ "success": success, "message": message, "data": data}, status=responseCode)
    
    
    def get(self, request, user_id=None):
        success = False
        data = None
        message = ''
        response_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        if user_id is not None:
            try:
                user = TblUser.objects.get(id=user_id)
                user_serializer = GetUserDetailsSerializer(instance=user)
                data = user_serializer.data
                success = True
                message = "Data Fetched"
                response_code = status.HTTP_200_OK

            except TblUser.DoesNotExist:
                message = "User Not Found"
                response_code = status.HTTP_404_NOT_FOUND

        else:
            all_users = TblUser.objects.all()
            all_users_serializer = GetUserDetailsSerializer(instance=all_users, many=True) 
            data = all_users_serializer.data
            success = True
            message = "Data Fetched"
            response_code = status.HTTP_200_OK
        
        print({
            "success": success,
            "data": data,
            "message": message,
            "response_code": response_code
        })

        # return Response({"success": success, "message": message, "data": data}, status=response_code)
        return render(request, 'userpage.html', {
            "success": success,
            "data": data,
            "message": message,
            "response_code": response_code
        })


class LoginView(APIView):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        user_login_serializer = LoginUserSerializer(data=request.data)
        if user_login_serializer.is_valid():
            email = user_login_serializer.validated_data['email']
            password = user_login_serializer.validated_data['password']

            try:
                user = TblUser.objects.get(email = email, is_active = True)
            except TblUser.DoesNotExist:
                # return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
                return render(request, 'login.html', {'error': 'Invalid credentials'})
            
            if check_password(password, user.password):
                django_user, created = User.objects.get_or_create(username = user.email)
                if created:
                    django_user.set_password(password)
                    django_user.save()
                refresh = RefreshToken.for_user(django_user)
                # return Response({
                #     'refresh': str(refresh),
                #     'access': str(refresh.access_token),
                #     'message': "Login Successful"
                # })
                user_id = user.id
                request.session['access_token'] = str(refresh.access_token)
                return redirect('user_details', user_id=user_id)
            else: 
                # return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED) 
                return render(request, 'login.html', {'error': 'Invalid credentials'})
        
        # return Response(user_login_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return render(request, 'login.html', {'error': user_login_serializer.errors})
                


# from rest_framework.generics import ListAPIView, RetrieveAPIView
# Restframework Generics
# Get all users                
# class UserListView(ListAPIView):
#     queryset = TblUser.objects.all()
#     serializer_class = UserSerializer
                

# Get individual user
# class UserDetailView(RetrieveAPIView):
#     queryset = TblUser.objects.all()
#     serializer_class = UserSerializer
#     lookup_field = 'id'

    
