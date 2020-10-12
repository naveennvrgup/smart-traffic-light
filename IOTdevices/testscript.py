from maps.models import *

def run():
    for x in TrafficSignal.objects.all():
        x.createTopic()
    # TrafficLight.objects.all()[0].createSubscription()