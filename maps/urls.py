from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('getRoute/', SmartRouteView),
    path('allSignals/', AllTrafficSignalsView),
    path('allHospitals/', AllHospitalsView),
]
