from google.cloud import pubsub_v1

SIGNAL_TOPIC_ID = "traffic-signals"
PROJECT_ID = "smart-traffic-lights-290011"

def publishToSignalTopic(msg):
    
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, SIGNAL_TOPIC_ID)

    msg = msg.encode("utf-8")
    future = publisher.publish(topic_path, msg)
    print(future.result())