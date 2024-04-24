from rest_framework import serializers
from .models import TblUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblUser
        fields = '__all__'


class GetUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblUser
        fields = ["first_name", "last_name", "email", "is_active", "is_deleted"]


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            return attrs
        else:
            raise serializers.ValidationError("Email and password are required.")