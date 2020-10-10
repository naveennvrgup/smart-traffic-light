from django.contrib import admin
from django.urls import path, include
from .views import *
from django.views.generic import TemplateView

urlpatterns = [
    path('getRoute/', SmartRouteView),
    path('allSignals/', AllTrafficSignalsView),
    path('allHospitals/', AllHospitalsView),
    path('turnSignalNormal/<int:signalId>/', TurnTrafficSignalNormalView),
    path('onHospitalRoute/<int:routeId>/', OnHospitalRouteView),
    path('stateReporting/', StateReportingView),
    path('reporting/',TemplateView.as_view(template_name='index.html')),
]
