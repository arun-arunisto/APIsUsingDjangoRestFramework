from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import TodoApi
from .serializers import TodoSerializer

# Create your views here.
class TodoListApiView(APIView):
    #1. List all
    def get(self, request, *args, **kwargs):
        todos = TodoApi.objects.all()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    #2. Create
    def post(self, request, *args, **kwargs):
        data = {
            "todo":request.data.get("todo"),
            "completed":request.data.get("completed")
        }
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TodoDetailApiView(APIView): #to detail view of an single todo
    def get_object(self, todo_id):
        try:
            return TodoApi.objects.get(id=todo_id)
        except TodoApi.DoesNotExist:
            return None

    def get(self,request,  todo_id):
        #retrieves the todo with given todo_id
        todo_instance = self.get_object(todo_id)
        if not todo_instance:
            return Response(
                {"res":"Object with todo id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = TodoSerializer(todo_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #update
    def put(self, request, todo_id, *args, **kwargs):
        todo_instance = self.get_object(todo_id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            "todo":request.data.get("todo"),
            "completed":request.data.get("completed")
        }
        serializer = TodoSerializer(instance=todo_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #delete
    def delete(self, request, todo_id, *args, **kwargs):
        todo_instance = self.get_object(todo_id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        todo_instance.delete()
        return Response(
            {"res":"Object deleted!"}
        )


