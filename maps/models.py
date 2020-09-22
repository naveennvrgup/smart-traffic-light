from django.db import models

# Create your models here.
class TrafficSignal(models.Model):
    location=models.CharField(max_length=100)
    lat=models.DecimalField(max_digits=9, decimal_places=6)
    long=models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f"{self.location} - ({self.lat},{self.long})"

class TrafficLight(models.Model):
    signal=models.ForeignKey(TrafficSignal, on_delete=models.CASCADE)
    direction=models.IntegerField()

    def __str__(self):
        return f"{self.direction} - {self.signal}"