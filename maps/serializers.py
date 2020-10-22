from rest_framework import serializers

from .models import *


class RoutingSerializer(serializers.Serializer):
    originLat = serializers.FloatField(allow_null=False)
    originLng = serializers.FloatField(allow_null=False)
    destination = serializers.CharField(allow_null=False)


class TrafficLightSerializer(serializers.ModelSerializer):
    operationMode = serializers.SerializerMethodField()
    signalState = serializers.SerializerMethodField()

    def get_operationMode(self, obj):
        return obj.get_operationMode_display()

    def get_signalState(self, obj):
        return obj.get_signalState_display()

    class Meta:
        model = TrafficLight
        fields = '__all__'


class TrafficSignalSerializer(serializers.ModelSerializer):
    lights = serializers.SerializerMethodField()

    def get_lights(self, obj: TrafficSignal):
        return TrafficLightSerializer(obj.trafficlight_set.all(), many=True).data

    class Meta:
        model = TrafficSignal
        fields = '__all__'


class SetTrafficLightStateBody(serializers.ModelSerializer):
    signalState = serializers.CharField(required=True)
    id = serializers.IntegerField(required=True)

    class Meta:
        model = TrafficLight
        fields = ['signalState', 'id']


class SetTrafficLightModeBody(serializers.ModelSerializer):
    operationMode = serializers.CharField(required=True)
    id = serializers.IntegerField(required=True)

    class Meta:
        model = TrafficLight
        fields = ['operationMode', 'id']


class HeartBeatBody(serializers.ModelSerializer):
    heartbeat = serializers.DateTimeField(required=True)

    class Meta:
        model = TrafficLight
        fields = ['heartbeat', 'id']
