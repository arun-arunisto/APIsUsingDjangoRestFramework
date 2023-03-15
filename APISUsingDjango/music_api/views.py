from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework_jwt.settings import api_settings
from .decorators import validate_request_data
from .models import Tracks
from .serializers import TrackSerializer, TokenSerializer, UserSerializer, RegisterSerializer


# Create your views here.
#JWT settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class ListCreateSongsView(generics.ListCreateAPIView):
    queryset = Tracks.objects.all()
    serializer_class = TrackSerializer
    permission_classes = (permissions.IsAuthenticated,) #checking that user is authenticated

    @validate_request_data #the function that we created in decorators.py
    def post(self, request, *args, **kwargs):
        a_song = Tracks.objects.create(
            title=request.data["title"],
            artist=request.data["artist"]
        )
        return Response(data=TrackSerializer(a_song).data,
                        status=status.HTTP_201_CREATED)

class TrackDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tracks.objects.all()
    serializer_class = TrackSerializer

    #get single track
    def get(self, request, *args, **kwargs):
        try:
            a_song = self.queryset.get(pk=kwargs["pk"])
            return Response(TrackSerializer(a_song).data)
        except Tracks.DoesNotExist:
            return Response(
                data={
                    "message":"Track id {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @validate_request_data
    #update
    def put(self, request, *args, **kwargs):
        try:
            a_song = self.queryset.get(pk=kwargs["pk"])
            serializer = TrackSerializer()
            updated_song = serializer.update(a_song, request.data)
            return Response(TrackSerializer(updated_song).data)
        except Tracks.DoesNotExist:
            return Response(
                data={
                    "message":"Track id {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    #delete
    def delete(self, request, *args, **kwargs):
        try:
            a_song = self.queryset.get(pk=kwargs["pk"])
            a_song.delete()
            return Response(status=status.HTTP_200_OK)
        except Tracks.DoesNotExist:
            return Response(
                data={
                    "message":"Tracks id {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

#users login
class LoginView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            serializer = TokenSerializer(data={
                'token':jwt_encode_handler(jwt_payload_handler(user))
            })
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

#reegister
class RegisterUsers(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer
    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        email = request.data.get("email", "")
        if not username and not password and not email:
            return Response(
                data={
                    "message":"Username, password and email is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        new_user = User.objects.create_user(
            username=username, password=password, email=email
        )
        return Response(
            data=UserSerializer(new_user).data,
            status=status.HTTP_201_CREATED
        )