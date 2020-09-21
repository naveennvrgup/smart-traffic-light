from django.contrib import admin
from django.urls import path, include
from users.views import *

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('authCheck/', AuthCheckView.as_view()),
]
