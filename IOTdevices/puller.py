from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1

# TODO(developer)

project_id = "smart-traffic-lights-290011"
subscription_id = "sub-traffic-signals"
# Number of seconds the subscriber should listen for messages
timeout = 3600

subscriber = pubsub_v1.SubscriberClient()
# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_id}`
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message):
    print("Received message: {}".format(message))
    message.ack()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print("Listening for messages on {}..\n".format(subscription_path))

# Wrap subscriber in a 'with' block to automatically call close() when done.
with subscriber:
    try:
        # When `timeout` is not set, result() will block indefinitely,
        # unless an exception is encountered first.
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        streaming_pull_future.cancel()

