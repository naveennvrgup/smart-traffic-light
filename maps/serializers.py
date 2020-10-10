from rest_framework import serializers
from .models import *

class RoutingSerializer(serializers.Serializer):
    originLat = serializers.FloatField(allow_null=False)
    originLng = serializers.FloatField(allow_null=False)
    destination = serializers.CharField(allow_null=False)


class TrafficLightSerializer(serializers.ModelSerializer):
    operationMode  = serializers.SerializerMethodField()
    signalState = serializers.SerializerMethodField() 

    def get_operationMode(self,obj):
        return obj.get_operationMode_display()

    def get_signalState(self,obj):
        return obj.get_signalState_display()
    
    class Meta:
        model = TrafficLight
        fields='__all__'


class TrafficSignalSerializer(serializers.ModelSerializer):
    operationMode  = serializers.SerializerMethodField()

    def get_operationMode(self,obj):
        return obj.get_operationMode_display()

    class Meta:
        model = TrafficSignal
        fields='__all__'