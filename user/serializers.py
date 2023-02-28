from rest_framework import serializers
from.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

class UserVerifySerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
    class Meta:
        model = User
        fields = ['email','otp']