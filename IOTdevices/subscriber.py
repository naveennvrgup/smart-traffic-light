from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
from publisher import SIGNAL_TOPIC_ID, PROJECT_ID


def subscribeToSignal(id):
    timeout = 3600
    SUBSCRIPTION_ID = f"signal{id}"

    subscriber = pubsub_v1.SubscriberClient()
    publisher = pubsub_v1.PublisherClient()

    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)
    topic_path=  publisher.topic_path(PROJECT_ID, SIGNAL_TOPIC_ID)
    
    subscription = subscriber.create_subscription(
        request={"name": subscription_path, "topic": topic_path}
    )
    
    def callback(message):
        print("Received message: {}".format(message))
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print("Listening for messages on {}..\n".format(subscription_path))

    streaming_pull_future.result()

    # with subscriber:
    #     try:
    #         # When `timeout` is not set, result() will block indefinitely,
    #         # unless an exception is encountered first.
    #         streaming_pull_future.result(timeout=timeout)
    #     except TimeoutError:
    #         streaming_pull_future.cancel()

if __name__ == "__main__":
    subscribeToSignal(1)
