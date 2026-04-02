from django.shortcuts import render
from rest_framework import generics
from rest_framework.generics import GenericAPIView
from rest_framework import status
from .serializers import *
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
# Create your views here.



class RegisterAPIView(GenericAPIView):
    
    serializer_class = RegisterSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save() 
        return Response(
            {
                "message": "User registered successfully",
                "data": serializer.data
            },status=status.HTTP_201_CREATED)
        


class LoginView(GenericAPIView):
    
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")
        user = authenticate(username=email, password=password)
        if user is None:
            return Response(
                {"error": "Invalid email or password"},
                status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        return Response({
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),})
