from rest_framework import serializers



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(allow_blank=False)
    password = serializers.CharField(allow_blank=False)

