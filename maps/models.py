from django.db import models
from django.utils.translation import gettext_lazy as _


class OperationMode(models.TextChoices):
    NORMAL = 'NL', _("Normal")
    OVERRIDE = 'OR', _("OverRide")


class SignalState(models.TextChoices):
    RED = 'RD', _("Red")
    GREEN = 'GR', _("Green")


class TrafficSignal(models.Model):
    location=models.CharField(max_length=100)
    lat=models.DecimalField(max_digits=9, decimal_places=6)
    lng=models.DecimalField(max_digits=9, decimal_places=6)
    
    controlList=models.JSONField(default=list)
    controlIndex=models.IntegerField(default=0)
    operationMode=models.CharField(max_length=2,choices=OperationMode.choices,default=OperationMode.NORMAL)
    timer=models.TimeField(auto_now=True)

    def __str__(self):
        return f"#{self.id} - {self.location} - ({self.lat},{self.lng})"


class TrafficLight(models.Model):
    signal=models.ForeignKey(TrafficSignal, on_delete=models.CASCADE)
    direction=models.IntegerField()
    
    operationMode=models.CharField(max_length=2,choices=OperationMode.choices,default=OperationMode.NORMAL)
    signalState=models.CharField(max_length=2,choices=SignalState.choices,default=SignalState.RED)

    def __str__(self):
        return f"#{self.id} - {self.direction} - {self.signal}"


class Hospital(models.Model):
    location=models.CharField(max_length=100)
    lat=models.DecimalField(max_digits=9, decimal_places=6)
    lng=models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f"#{self.id} - {self.location} - ({self.lat},{self.lng})"