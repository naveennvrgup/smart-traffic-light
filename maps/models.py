from django.db import models
from django.utils.translation import gettext_lazy as _
from server.settings import PROJECT_ID, subscriber, publisher


class OperationMode(models.TextChoices):
    NORMAL = 'NL', _("Normal")
    OVERRIDE = 'OR', _("OverRide")


class SignalState(models.TextChoices):
    RED = 'RD', _("Red")
    GREEN = 'GR', _("Green")


def controlListDefault():
    return [[]]

    
class TrafficSignal(models.Model):
    location=models.CharField(max_length=100)
    lat=models.DecimalField(max_digits=9, decimal_places=6, default=0)
    lng=models.DecimalField(max_digits=9, decimal_places=6, default=0)
    
    controlList=models.JSONField(default=controlListDefault)
    controlIndex=models.IntegerField(default=0)
    operationMode=models.CharField(max_length=2,choices=OperationMode.choices,default=OperationMode.NORMAL)
    timer=models.TimeField(auto_now=True)


    def __str__(self):
        return f"#{self.id} - {self.location} - ({self.lat},{self.lng})"


    def getTopicID(self):
        return "STS"+str(self.id).zfill(5)


    def createTopic(self):
        TOPIC_ID= self.getTopicID()
        topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

        try:
            topic = publisher.create_topic(request={"name": topic_path})
            print(f"created topic {TOPIC_ID}")
        except Exception as err:
            print(err)


    def deleteTopic(self):
        topic_path = publisher.topic_path(PROJECT_ID, self.getTopicID())

        try:
            publisher.delete_topic(request={"topic": topic_path})
            print(f"deleted topic {self.getTopicID()}")
        except Exception as err:
            print(err)



class TrafficLight(models.Model):
    signal=models.ForeignKey(TrafficSignal, on_delete=models.CASCADE)
    direction=models.IntegerField()
    
    operationMode=models.CharField(max_length=2,choices=OperationMode.choices,default=OperationMode.NORMAL)
    signalState=models.CharField(max_length=2,choices=SignalState.choices,default=SignalState.RED)


    def __str__(self):
        return f"#{self.id} - {self.direction} - {self.signal}"


    def getSubscriptionID(self):
        return "STL"+str(self.id).zfill(5)


    def createSubscription(self):    

        # subscriber = pubsub_v1.SubscriberClient()
        # publisher = pubsub_v1.PublisherClient()
        
        SUBSCRIPTION_ID= self.getSubscriptionID()
        TOPIC_ID = self.signal.getTopicID()
        
        subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)
        topic_path=  publisher.topic_path(PROJECT_ID, TOPIC_ID)

        try:
            subscription = subscriber.create_subscription(
                request={"name": subscription_path, "topic": topic_path}
            )
            print(f"created subscription {SUBSCRIPTION_ID}")
        except Exception as err:
            print(err)


    def deleteSubscription(self):
        # subscriber = pubsub_v1.SubscriberClient()
        subscription_path = subscriber.subscription_path(PROJECT_ID, self.getSubscriptionID())

        try:
            subscriber.delete_subscription(request={"subscription": subscription_path})
            print(f"deleted subscription {self.getSubscriptionID()}")
        except Exception as err:
            print(err)


class Hospital(models.Model):
    location=models.CharField(max_length=100)
    lat=models.DecimalField(max_digits=9, decimal_places=6)
    lng=models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f"#{self.id} - {self.location} - ({self.lat},{self.lng})"
