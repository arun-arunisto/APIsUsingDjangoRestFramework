from rest_framework import serializers
from django.contrib.auth.models import User
#user we used for the authentification

from .models import Tracks

class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tracks
        fields = ("title", "artist", "uploaded_at")


class TokenSerializer(serializers.Serializer):
    #this serializer serializes the token data
    token = serializers.CharField(max_length=255)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password")

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password", "email")

