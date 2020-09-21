from django.shortcuts import render
from . import responses 
from .serializers import LoginSerializer
from rest_framework.views import APIView
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from utils.swagger import set_example
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


class LoginView(APIView):
    @swagger_auto_schema(
        operation_id='login_user',
        request_body=LoginSerializer,
        responses={
            '202': set_example(responses.login_202),
            '400': set_example(responses.login_400),
            '401': set_example(responses.login_401),
            '404': set_example(responses.login_404)
        },
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = authenticate(
                username=serializer.data['username'],
                password=serializer.data['password']
                )     
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': f"Token {token.key}"}, status.HTTP_202_ACCEPTED)
            else:
                try:
                    if User.objects.get(username=serializer.data['username']):
                        return Response({'detail': 'Credentials did not match'}, status.HTTP_401_UNAUTHORIZED)
                    
                except User.DoesNotExist:
                    return Response({"detail": "User not found"}, status.HTTP_404_NOT_FOUND)     
        else:
            data = serializer.errors
            return Response(data, status.HTTP_400_BAD_REQUEST)


class AuthCheckView(APIView):
    permission_classes = [IsAuthenticated]


    @swagger_auto_schema(
        operation_id='auth_check',
        responses={
            '200': set_example(responses.auth_check_200),
            '401': set_example(responses.unauthenticated_401),
        },
    )
    def get(self, request):
        return Response("You are authenticated")