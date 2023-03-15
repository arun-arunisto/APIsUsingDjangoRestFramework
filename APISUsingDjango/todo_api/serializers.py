from rest_framework import serializers
from .models import TodoApi

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoApi
        fields = ["todo", "timestamp", "completed", "updated"]