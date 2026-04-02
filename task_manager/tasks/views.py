from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import *
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.pagination import PageNumberPagination
from .task import task_created_notification
# Create your views here.


class CreateTaskAPI(GenericAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    
    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save(user=request.user)
        task_created_notification.delay(task.user.id, task.title)
        return Response(
            {
                "message": "Task created successfully",
                "data": serializer.data
            },status=status.HTTP_201_CREATED)
        
        

class TaskListAPI(GenericAPIView):
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
    parameters=[
        OpenApiParameter(
            name="status",
            description="Filter tasks by status (PENDING or COMPLETED)",
            required=False,
            type=str
        ),
    ]
)
    
    def get(self,request):
        tasks = Task.objects.filter(user=request.user).order_by('-created_at')
        status_param = request.query_params.get('status')
        if status_param:
            tasks = tasks.filter(status=status_param.upper())
        paginator = PageNumberPagination()
        paginator.page_size = 5
        paginated_task = paginator.paginate_queryset(tasks,request)
        serializer = self.get_serializer(paginated_task,many=True)
        return paginator.get_paginated_response(serializer.data)
    
    
    
class TaskDetailAPI(GenericAPIView):
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self,request,pk):
        try:
            task = Task.objects.get(pk=pk,user=request.user)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=404)
        serializer = self.get_serializer(task)
        return Response(serializer.data)
    
    
    
class TaskUpdateAPI(GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return TaskUpdateSerializer
        elif self.request.method == 'PATCH':
            return TaskStatusUpdateSerializer   
        return TaskUpdateSerializer
    
    @extend_schema(request=TaskUpdateSerializer, responses=TaskUpdateSerializer)
    
    def put(self,request,pk):
        try:
            task = Task.objects.get(pk=pk,user=request.user)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=404)
        serializer = self.get_serializer(task,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": "Task updated successfully",
            "data": serializer.data}, status=status.HTTP_200_OK)
        
        
        
    @extend_schema(request=TaskStatusUpdateSerializer, responses=TaskStatusUpdateSerializer)
       
    def patch(self,request,pk):
        try:
            task = Task.objects.get(pk=pk,user=request.user)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=404)
        serializer = self.get_serializer(task,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": "Task status change successfully",
            "data": serializer.data}, status=status.HTTP_200_OK)
        
        
        
class TaskDeleteAPI(GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(responses={200: {"type": "object", "properties":  
        {"message": {"type": "string"}}}})
    
    def delete(self,request,pk):
        try:
            task = Task.objects.get(pk=pk,user=request.user)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=404)
        task.delete()
        return Response(
            {"message": "Task deleted successfully"},
            status=status.HTTP_200_OK
        )
        
