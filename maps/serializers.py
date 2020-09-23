from rest_framework import serializers


class RoutingSerializer(serializers.Serializer):
    originLat = serializers.FloatField(allow_null=False)
    originLng = serializers.FloatField(allow_null=False)
    destination = serializers.CharField(allow_null=False)
