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
import math

def findBearing(lat1,lon1,lat2,lon2):
    # bearing is the between line formed by source,destination and north
    dLon = lon2 - lon1
    y = math.sin(dLon) * math.cos(lat2)
    x = math.cos(lat1)*math.sin(lat2) - math.sin(lat1)*math.cos(lat2)*math.cos(dLon)
    brng = math.degrees(math.atan2(y, x))
    if brng<0: brng+=360

    return int(brng)



def isPointOnRoute(wayPoints, trafficSignal):
    n=len(wayPoints)
    trafficLightsEnroute=[]
    
    for i in range(n):
        currWayPoint=wayPoints[i]
    
        # if the geoPoint is within 10m of wayPoint we can consider the geoPoint to be "in route"
        if geodesic(currWayPoint,(trafficSignal.lat,trafficSignal.lng)).meters <= 10:
            trafficLights = TrafficLight.objects.filter(signal=trafficSignal)

            # signal from
            j=i-1
            while j>=0 and geodesic(wayPoints[j],(trafficSignal.lat,trafficSignal.lng)).meters <= 50: 
                j-=1
                
            if j>=0:
                prevWayPoint=wayPoints[j]
                bearing=findBearing(currWayPoint[0], currWayPoint[1], prevWayPoint[0], prevWayPoint[1])
                diff=361
                correctTrafficLight=None

                for trafficLight in trafficLights:
                    currDiff=abs(trafficLight.direction-bearing)
                    if currDiff<diff:
                        correctTrafficLight=trafficLight
                        diff=currDiff

                trafficLightsEnroute.append(correctTrafficLight)
                print(f"bearing {trafficSignal}: {correctTrafficLight}")


            # signal to
            j=i+1
            while j<n and geodesic(wayPoints[j],(trafficSignal.lat,trafficSignal.lng)).meters <= 50: 
                j+=1

            if j<n:
                nxtWayPoint=wayPoints[j]
                bearing=findBearing(currWayPoint[0], currWayPoint[1], nxtWayPoint[0],nxtWayPoint[1])
                diff=361
                correctTrafficLight=None

                for trafficLight in trafficLights:
                    currDiff=abs(trafficLight.direction-bearing)
                    if currDiff<diff:
                        correctTrafficLight=trafficLight
                        diff=currDiff

                trafficLightsEnroute.append(correctTrafficLight)
                print(f"bearing {trafficSignal}: {correctTrafficLight}")
                
            break # after finding the traffic junction for the particular traffic light no need to loop again

    return trafficLightsEnroute



class RoutingView(APIView):
    permission_classes=[IsAuthenticated]

    @swagger_auto_schema(
        operation_id='smart_route',
        request_body=RoutingSerializer,
        responses={
            401: set_example(responses.unauthenticated_401),
            200: set_example(responses.smart_route_200),
        },
    )
    def post(self, request):
        """
            sample request 
            {
            "originLat": 11.215659,
            "originLng": 77.357261,
            "destination": "puluapatti, Tiruppur, Tamil Nadu"
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
        print(f"\n----geoCodeDestinationAPI---")
        print(geoCodeDestinationAPI)
        
        # call geo code API
        geoCodeDestinationAPIResponse = requests.get(geoCodeDestinationAPI).json()
        destinationPosition=geoCodeDestinationAPIResponse['hits'][0]['point']
        destinationLat=destinationPosition['lat']
        destinationLng=destinationPosition['lng']
        print(f"\n----geoCodeDestinationAPIResponse---")
        print(f'[destinationLat,destinationLng]: [{destinationLat},{destinationLng}]')


        # prepare destinationroute API
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
        print(f"\n----routeAPI---")
        print(routeAPI)


        # call route API
        routeAPIResponse = requests.get(routeAPI).json()
        routeAPIResponse=routeAPIResponse['paths'][0]
        wayPoints=polyline.decode(routeAPIResponse['points'])
        print(f"\n----routeAPIResponse---")
        print(routeAPIResponse)



        # print waypoint for dev test plotting
        print(f"\n---waypoint--{len(wayPoints)}----")
        for wayPoint in wayPoints:
            print(f"{wayPoint[0]},{wayPoint[1]}")
        print(f"\n---traffic signals on point----")
    
                
        # smart traffic signals on the path
        allTrafficSignals= TrafficSignal.objects.all()
        trafficSignalsOnPath = []
        trafficLightsOnPath = []
        for trafficSignal in allTrafficSignals:
            curr=isPointOnRoute(wayPoints, trafficSignal)
            
            if len(curr)>0:
                trafficSignalsOnPath.append({
                    'lat':trafficSignal.lat,
                    'lng':trafficSignal.lng,
                    'location':trafficSignal.location
                })
                for trafficLight in curr:
                    trafficLightsOnPath.append({
                        'lat':trafficSignal.lat,
                        'lng':trafficSignal.lng,
                        'direction':trafficLight.direction,
                        'location':trafficSignal.location,
                    })

        # prepare the smart route response
        smartRouteResponse={
            'distanceKms': round(routeAPIResponse['distance']/1000,1),
            'timeMins': routeAPIResponse['time']/60//1000,
            'polyline':routeAPIResponse['points'],
            'trafficSignalsOnPath': trafficSignalsOnPath,
            'trafficLightsOnPath': trafficLightsOnPath,
            'wayPoints': wayPoints,
        }


        return Response(smartRouteResponse, status.HTTP_200_OK)



class AllTrafficSignalsView(APIView):
    permission_classes=[IsAuthenticated]

    @swagger_auto_schema(
        operation_id='registered_smart_traffic_signals',
        responses={
            401: set_example(responses.unauthenticated_401),
        },
    )
    def get(self, request):
        allTrafficSignals = [[x.lat,x.lng] for x in TrafficSignal.objects.all()]
        return Response(allTrafficSignals, status.HTTP_200_OK)