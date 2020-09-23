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
from .models import *
from geopy.distance import geodesic



def isPointOnRoute(wayPoints, lat, lng):
    for waypoint in wayPoints:
        # if the geoPoint is within 10m of wayPoint we can consider the geoPoint to be "in route"
        if geodesic(waypoint,(lat,lng)).meters <= 10:
            print(f"{lat},{lng}")
            return True
    return False



class RoutingView(APIView):
    permission_classes=[IsAuthenticated]

    @swagger_auto_schema(
        operation_id='smart_route',
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
                "originLng": 77.5440772,
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
        originLng=cleanData['originLng']

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
        destinationLng=destinationPosition['lng']
        print(f'[destinationLat,destinationLng]: [{destinationLat},{destinationLng}]')


        # prepare route API
        routeAPI = (
            f'https://graphhopper.com/api/1/route'
            f'?point={originLat},{originLng}'
            f'&point={destinationLat},{destinationLng}'
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
        wayPoints=polyline.decode(routeAPIResponse['points'])
        print(routeAPIResponse)



        # print waypoint for dev test plotting
        print(f"---waypoint--{len(wayPoints)}----")
        for wayPoint in wayPoints:
            print(f"{wayPoint[0]},{wayPoint[1]}")
        print(f"---traffic signals on point----")
    
                
        # smart traffic signals on the path
        allTrafficSignals= TrafficSignal.objects.all()
        trafficSignalsOnPath = []
        for trafficSignal in allTrafficSignals:
            if isPointOnRoute(wayPoints, trafficSignal.lat, trafficSignal.lng):
                trafficSignalsOnPath.append({
                    'lat': trafficSignal.lat,
                    'lng': trafficSignal.lng
                })

        # prepare the smart route response
        smartRouteResponse={
            'distance': routeAPIResponse['distance'],
            'distanceKms': round(routeAPIResponse['distance']/1000,1),
            'time': routeAPIResponse['time'],
            'timeMins': routeAPIResponse['time']/60//1000,
            'polyline':routeAPIResponse['points'],
            'trafficSignalsOnPath': trafficSignalsOnPath,
            'wayPoints': wayPoints,
        }
        print(len(smartRouteResponse['wayPoints']))
        

        return Response(smartRouteResponse)

