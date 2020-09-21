from rest_framework import serializers


class RoutingSerializer(serializers.Serializer):
    originLat = serializers.FloatField(allow_null=False)
    originLong = serializers.FloatField(allow_null=False)
    destination = serializers.CharField(allow_null=False)
