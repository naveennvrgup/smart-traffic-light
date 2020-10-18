import math
import traceback

import polyline
import requests
from decouple import config
from drf_yasg.utils import swagger_auto_schema
from geopy.distance import geodesic
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from utils.swagger import set_example
from . import responses
from .serializers import *


def findBearing(lat1, lon1, lat2, lon2):
    # bearing is the between line formed by source,destination and north
    dLon = lon2 - lon1
    y = math.sin(dLon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dLon)
    brng = math.degrees(math.atan2(y, x))
    if brng < 0: brng += 360

    return int(brng)


def isTrafficLightOnRoute(wayPoints, trafficSignal):
    n = len(wayPoints)
    trafficLightsEnroute = []

    for i in range(n):
        currWayPoint = wayPoints[i]

        # if the geoPoint is within 10m of wayPoint we can consider the geoPoint to be "in route"
        if geodesic(currWayPoint, (trafficSignal.lat, trafficSignal.lng)).meters <= 10:
            trafficLights = TrafficLight.objects.filter(signal=trafficSignal)

            # signal from
            j = i - 1
            while j >= 0 and geodesic(wayPoints[j], (trafficSignal.lat, trafficSignal.lng)).meters <= 50:
                j -= 1

            if j >= 0:
                prevWayPoint = wayPoints[j]
                bearing = findBearing(currWayPoint[0], currWayPoint[1], prevWayPoint[0], prevWayPoint[1])
                diff = 361
                correctTrafficLight = None

                for trafficLight in trafficLights:
                    currDiff = abs(trafficLight.direction - bearing)
                    if currDiff < diff:
                        correctTrafficLight = trafficLight
                        diff = currDiff

                trafficLightsEnroute.append(correctTrafficLight)
                print(f"bearing {trafficSignal}: {correctTrafficLight}")

            # signal to
            j = i + 1
            while j < n and geodesic(wayPoints[j], (trafficSignal.lat, trafficSignal.lng)).meters <= 50:
                j += 1

            if j < n:
                nxtWayPoint = wayPoints[j]
                bearing = findBearing(currWayPoint[0], currWayPoint[1], nxtWayPoint[0], nxtWayPoint[1])
                diff = 361
                correctTrafficLight = None

                for trafficLight in trafficLights:
                    currDiff = abs(trafficLight.direction - bearing)
                    if currDiff < diff:
                        correctTrafficLight = trafficLight
                        diff = currDiff

                trafficLightsEnroute.append(correctTrafficLight)
                print(f"bearing {trafficSignal}: {correctTrafficLight}")

            break  # after finding the traffic junction for the particular traffic light no need to loop again

    return trafficLightsEnroute


def geoCode(destination, apiKey):
    geoCodeDestinationAPI = (
        f'https://graphhopper.com/api/1/geocode'
        f'?q={destination}'
        f'&debug=true'
        f'&key={apiKey}'
    )

    # call geo code API
    geoCodeDestinationAPIResponse = requests.get(geoCodeDestinationAPI).json()
    destinationPosition = geoCodeDestinationAPIResponse['hits'][0]['point']
    destinationLat = destinationPosition['lat']
    destinationLng = destinationPosition['lng']

    print(f"\n----geoCodeDestinationAPIResponse---")
    print(f'[destinationLat,destinationLng]: [{destinationLat},{destinationLng}]')

    return [destinationLat, destinationLng]


def findRoute(lat1, lng1, lat2, lng2, apiKey):
    routeAPI = (
        f'https://graphhopper.com/api/1/route'
        f'?point={lat1},{lng1}'
        f'&point={lat2},{lng2}'
        f'&vehicle=car'
        f'&instructions=false'
        # f'&points_encoded=false'
        f'&alternative_route.max_paths=1'
        f'&key={apiKey}'
    )

    # call route API
    routeAPIResponse = requests.get(routeAPI).json()
    routeAPIResponse = routeAPIResponse['paths'][0]

    # format data
    routePolyline = routeAPIResponse['points']
    routeWayPoints = polyline.decode(routePolyline)
    travelDistance = round(routeAPIResponse['distance'] / 1000, 1)
    travelTime = routeAPIResponse['time'] / 60 // 1000

    # print waypoint for dev test plotting
    print(f"\n---waypoint--{len(routeWayPoints)}----")
    for wayPoint in routeWayPoints:
        print(f"{wayPoint[0]},{wayPoint[1]}")

    return (travelTime, travelDistance, routePolyline, routeWayPoints)


def findTrafficSignals(wayPoints):
    # smart traffic signals on the path
    allTrafficSignals = TrafficSignal.objects.all()
    trafficSignalsOnPath, trafficLightsOnPath = [], []

    print(f"\n----trafficsignals enroute---")

    for trafficSignal in allTrafficSignals:
        curr = isTrafficLightOnRoute(wayPoints, trafficSignal)

        # represents signal on route
        if len(curr) > 0:
            trafficSignalsOnPath.append({
                'id': trafficSignal.id,
                'lat': trafficSignal.lat,
                'lng': trafficSignal.lng,
                'location': trafficSignal.location
            })
            for trafficLight in curr:
                trafficLightsOnPath.append({
                    'id': trafficLight.id,
                    'lat': trafficSignal.lat,
                    'lng': trafficSignal.lng,
                    'direction': trafficLight.direction,
                    'location': trafficSignal.location,
                })

    return [trafficSignalsOnPath, trafficLightsOnPath]


def override_signals(signals, lights):
    for signal in signals:
        signal_obj = TrafficSignal.objects.get(id=signal)
        for light_obj in signal_obj.trafficlight_set.all():
            if light_obj.id in lights:
                light_obj.over_ride_to(GREEN)
            else:
                light_obj.over_ride_to(RED)


def findNearestHospital(lat, lng):
    hospitals = Hospital.objects.all()
    distance = math.inf
    nearestHospital = None

    for hospital in hospitals:
        curr = geodesic((hospital.lat, hospital.lng), (lat, lng))
        if curr < distance:
            nearestHospital = hospital
            distance = curr

    return nearestHospital


@swagger_auto_schema(
    operation_id='smart_route',
    request_body=RoutingSerializer,
    responses={
        401: set_example(responses.unauthenticated_401),
        200: set_example(responses.smart_route_200),
    },
    method='post'
)
@api_view(['post'])
@permission_classes([IsAuthenticated])
def SmartRouteView(request):
    """
        sample request 
        {
        "originLat": 11.215659,
        "originLng": 77.357261,
        "destination": "puluapatti, Tiruppur, Tamil Nadu"
        }
    """

    # check for valid input
    serializer = RoutingSerializer(data=request.data)
    if serializer.is_valid():
        cleanData = serializer.data
    else:
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    # prepare data
    apiKey = config('MAPS_API_KEY')
    destination = cleanData['destination']
    originLat = cleanData['originLat']
    originLng = cleanData['originLng']

    # get destination route info from api
    try:
        destinationLat, destinationLng = geoCode(destination, apiKey)
    except e:
        traceback.print_exc()
        return Response({'msg': 'error geocoding destination'}, status.HTTP_400_BAD_REQUEST)

    try:
        desTime, desDistance, destinationPolyline, destinationWaypoints = findRoute(originLat, originLng,
                                                                                    destinationLat, destinationLng,
                                                                                    apiKey)
    except:
        traceback.print_exc()
        return Response({'msg': 'error fetching destination route'}, status.HTTP_400_BAD_REQUEST)

    # find nearest hospital
    nearestHospital = findNearestHospital(destinationLat, destinationLng)

    # find hospital route info from api
    try:
        hospitalTime, hospitalDistance, hospitalPolyline, hospitalWaypoints = findRoute(
            destinationLat, destinationLng, nearestHospital.lat, nearestHospital.lng, apiKey)
    except:
        traceback.print_exc()
        return Response({'msg': 'error fetching hospital route'}, status.HTTP_400_BAD_REQUEST)

    # find traffic signals on path
    desSignals, desLights = findTrafficSignals(destinationWaypoints)
    hosSignals, hosLights = findTrafficSignals(hospitalWaypoints)

    # override the traffic lights on the destination route
    override_signals([x['id'] for x in desSignals], [x['id'] for x in desLights])

    # save the hospital route override in the future
    hos_route = HospitalRoute.objects.create(route_info={
        "signals": [x['id'] for x in hosSignals],
        "lights": [x['id'] for x in hosLights]
    })

    # prepare the smart route response
    smartRouteResponse = {
        'destinationTime': desTime,
        'hospitalTime': hospitalTime,

        'destinationDistance': desDistance,
        'hospitalDistance': hospitalDistance,

        'hospitalName': nearestHospital.location,
        'hospitalLat': nearestHospital.lat,
        'hospitalLng': nearestHospital.lng,
        'hospitalRouteId': hos_route.id,

        'destinationSignals': desSignals,
        'hospitalSignals': hosSignals,
        'destinationLights': desLights,
        'hospitalLights': hosLights,

        'destinationPolyline': destinationPolyline,
        'hospitalPolyline': hospitalPolyline,

        'destinationWayPoints': destinationWaypoints,
        'hospitalWayPoints': destinationWaypoints,
    }

    return Response(smartRouteResponse, status.HTTP_200_OK)


@swagger_auto_schema(
    operation_id='registered_smart_traffic_signals',
    responses={
        401: set_example(responses.unauthenticated_401),
    },
    method='get'
)
@api_view(['get'])
@permission_classes([IsAuthenticated])
def AllTrafficSignalsView(request):
    allTrafficSignals = [{
        'id': x.id,
        'lat': x.lat,
        'lng': x.lng,
        'name': x.location,
    } for x in TrafficSignal.objects.all()]

    print(f"\n----all trafficsignals---")
    for trafficSignal in allTrafficSignals:
        print(f"{trafficSignal['lat']},{trafficSignal['lng']}")

    return Response(allTrafficSignals, status.HTTP_200_OK)


@swagger_auto_schema(
    operation_id='registered_hospitals',
    responses={
        401: set_example(responses.unauthenticated_401),
    },
    method='get'
)
@api_view(['get'])
@permission_classes([IsAuthenticated])
def AllHospitalsView(request):
    allHospitals = [{
        'lat': x.lat,
        'lng': x.lng,
        'name': x.location,
    } for x in Hospital.objects.all()]

    print(f"\n----all hospitals---")
    for hospital in allHospitals:
        print(f"{hospital['lat']},{hospital['lng']}")

    return Response(allHospitals, status.HTTP_200_OK)


@swagger_auto_schema(
    operation_id='turn_traffic_signal_to_normal_state',
    responses={
        401: set_example(responses.unauthenticated_401),
    },
    method='get'
)
@api_view(['get'])
@permission_classes([IsAuthenticated])
def TurnTrafficSignalNormalView(request, signalId):
    print(signalId)

    return Response({'msg': 'Traffic Signal returned to normal'}, status.HTTP_200_OK)


@swagger_auto_schema(
    operation_id='turn_on_hospital_route',
    responses={
        401: set_example(responses.unauthenticated_401),
    },
    method='get'
)
@api_view(['get'])
@permission_classes([IsAuthenticated])
def OnHospitalRouteView(request, routeId):
    hospital_route_obj = HospitalRoute.objects.get(id=routeId).route_info
    signals = hospital_route_obj['signals']
    lights = hospital_route_obj['lights']
    override_signals(signals, lights)

    return Response({'msg': 'Switched to hospital route'}, status.HTTP_200_OK)


@api_view(['get'])
@permission_classes([AllowAny])
def StateReportingView(request):
    return Response({
        'trafficLights': TrafficLightSerializer(TrafficLight.objects.all(), many=True).data,
        'trafficSignals': TrafficSignalSerializer(TrafficSignal.objects.all(), many=True).data,
    }, status=status.HTTP_200_OK)
