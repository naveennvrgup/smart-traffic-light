from maps.models import *

def run():
    # for x in TrafficSignal.objects.all():
    #     # x.createTopic()
    #     x.createSubscription()
    #     # x.deleteTopic()

    for x in TrafficLight.objects.all():
        x.switchToNormalRide()