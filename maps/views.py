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
import polyline


class RoutingView(APIView):
    permission_classes=[IsAuthenticated]

    @swagger_auto_schema(
        operation_id='login_user',
        request_body=RoutingSerializer,
        responses={
            401: set_example(responses.unauthenticated_401),
        },
    )
    def post(self, request):
        """
            sample request from Banasankari,Banglore to Jayanagar,Banglore
            {
                "originLat": 12.9292674,
                "originLong": 77.5440772,
                "destination": "Jayanagar,Banglore"
            }
        """

        # check for valid input
        serializer=RoutingSerializer(data=request.data)
        if serializer.is_valid():
            cleanData = serializer.data
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


        # prepare geo code API
        apiKey=config('MAPS_API_KEY')
        destination=cleanData['destination']
        originLat=cleanData['originLat']
        originLong=cleanData['originLong']

        geoCodeDestinationAPI=(
            f'https://graphhopper.com/api/1/geocode'
            f'?q={destination}'
            f'&debug=true'
            f'&key={apiKey}'
        )
        print(geoCodeDestinationAPI)
        
        # call geo code API
        geoCodeDestinationAPIResponse = requests.get(geoCodeDestinationAPI).json()
        destinationPosition=geoCodeDestinationAPIResponse['hits'][0]['point']
        destinationLat=destinationPosition['lat']
        destinationLong=destinationPosition['lng']
        print(f'[destinationLat,destinationLong]: [{destinationLat},{destinationLong}]')


        # prepare route API
        routeAPI = (
            f'https://graphhopper.com/api/1/route'
            f'?point={originLat},{originLong}'
            f'&point={destinationLat},{destinationLong}'
            f'&vehicle=car'
            f'&instructions=false'
            # f'&points_encoded=false'
            f'&alternative_route.max_paths=1'
            f'&key={apiKey}'
        )
        print(routeAPI)


        # call route API
        routeAPIResponse = requests.get(routeAPI).json()
        routeAPIResponse=routeAPIResponse['paths'][0]
        print(routeAPIResponse)

        

        # prepare the smart route response
        smartRouteResponse={
            'distance': routeAPIResponse['distance'],
            'distanceKms': round(routeAPIResponse['distance']/100,1),
            'time': routeAPIResponse['time'],
            'timeMins': routeAPIResponse['time']/60//1000,
            'polyline':routeAPIResponse['points'],
            'smartTrafficLights': ['still on works will have to do this algo'],
            'points': polyline.decode(routeAPIResponse['points']),
        }
        print(len(smartRouteResponse['points']))
        return Response(smartRouteResponse)

