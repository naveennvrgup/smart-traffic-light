from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('getRoute/', RoutingView.as_view()),
    path('allSignals/', AllTrafficSignalsView.as_view()),
]
