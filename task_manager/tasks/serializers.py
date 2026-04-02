from rest_framework import serializers
from .models import Task
from datetime import date
from accounts.models import User


class TaskSerializer(serializers.ModelSerializer):
    
    status = serializers.ChoiceField(
        choices=[('PENDING', 'Pending'), ('COMPLETED', 'Completed')],
        error_messages={
            "invalid_choice": "Status must be PENDING or COMPLETED",
            "required": "Status is required"
        }
    )
    
    class Meta:
        
        model = Task
        
        fields = ['id', 'title', 'description', 'status', 'due_date']
        
        read_only_fields = ['user']
        
        
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value
    
        
    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title is required")
        return value
    

    def validate_due_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Due date cannot be in the past")
        return value
    
    
    def validate_status(self, value):
        if value not in ['PENDING', 'COMPLETED']:
            raise serializers.ValidationError("Invalid status")
        return value
    
    
    
class TaskListSerializer(serializers.ModelSerializer):
    
    created_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    updated_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    
    class Meta:
        
        model = Task
        
        fields = ["id","title","description","due_date","status","user","created_at",
                  "updated_at",]
        
        read_only_fields = ['user']
        
        
        
class TaskUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model = Task
        
        fields = ['title', 'description', 'due_date','status']
        

    def validate_due_date(self, value):
        from datetime import date
        if value < date.today():
            raise serializers.ValidationError("Due date cannot be in the past")
        return value
    
    
    
class TaskStatusUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model = Task
        
        fields = ['status']