from django.urls import path
from .views import *


urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    
    path("login/", LoginView.as_view()),
    
]
