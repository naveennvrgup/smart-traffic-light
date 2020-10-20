from django.urls import path
from django.views.generic import TemplateView

from .views import *

urlpatterns = [
    path('getRoute/', SmartRouteView),
    path('allSignals/', AllTrafficSignalsView),
    path('allHospitals/', AllHospitalsView),
    path('turnSignalNormal/<int:signalId>/', TurnTrafficSignalNormalView),
    path('onHospitalRoute/<int:routeId>/', OnHospitalRouteView),
    path('stateReporting/', StateReportingView),
    path('revokeOverRide/', RevokeOverRideView),
    path('reporting/', TemplateView.as_view(template_name='index.html')),
]
