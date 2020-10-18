from maps.models import *
from .actions import *


def delete_override():
    for x in TrafficLight.objects.all():
        x.switch_to_normal_ride()


def test_override():
    TrafficLight.objects.all()[0].over_ride_to(GREEN)


def run():
    # test_override()
    delete_override()
    print("done")
