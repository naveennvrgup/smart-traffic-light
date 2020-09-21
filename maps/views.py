from django.shortcuts import render
from . import responses 
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from utils.swagger import set_example
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from decouple import config
import requests


class RoutingView(APIView):
    permission_classes=[IsAuthenticated]

    @swagger_auto_schema(
        operation_id='login_user',
        request_body=RoutingSerializer,
        responses={
            401: set_example(responses.unauthenticated_401),
            404: set_example(responses.route_failed_400),
        },
    )
    def post(self, request):
        # check for valid input
        serializer=RoutingSerializer(data=request.data)
        if serializer.is_valid():
            cleanData = serializer.data
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


        # prepare geo code API
        apiKey=config('HERE_MAPS_API_KEY')
        destination=cleanData['destination']
        originLat=cleanData['originLat']
        originLong=cleanData['originLong']

        geoCodeDestinationAPI=(
            f"https://geocode.search.hereapi.com/v1/geocode"
            f"?q={destination},Bengaluru,Karnataka,India"
            f"&apiKey={apiKey}"
        )
        print(geoCodeDestinationAPI)
        
        # call geo code API
        geoCodeDestinationAPIResponse = requests.get(geoCodeDestinationAPI).json()
        destinationPosition=geoCodeDestinationAPIResponse['items'][0]['position']
        destinationLat=destinationPosition['lat']
        destinationLong=destinationPosition['lng']
        print(f'destinationLat:{destinationLat} destinationLong:{destinationLong}')


        # prepare route API
        routeAPI = (
            f'https://router.hereapi.com/v8/routes'
            f'?transportMode=car'
            f'&origin={originLat},{originLong}'
            f'&destination={destinationLat},{destinationLong}'
            f'&return=polyline,summary'
            f'&apiKey={apiKey}'
        )
        print(routeAPI)


        # call route API
        routeAPIResponse = requests.get(routeAPI).json()

        if len(routeAPIResponse['routes'])==0:
            return Response(routeAPIResponse['notices'], status.HTTP_400_BAD_REQUEST)


        return Response(routeAPIResponse)

