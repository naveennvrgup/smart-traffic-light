from google.cloud import pubsub_v1

# python cloudiot_pubsub_example_mqtt_device.py \
#     --project_id=smart-traffic-lights-290011 \
#     --registry_id=SmartTrafficLights \
#     --device_id=sheldon \
#     --private_key_file=rsa_private.pem \
#     --algorithm=RS256

# export GOOGLE_APPLICATION_CREDENTIALS="/home/naveen/Desktop/python-docs-samples/iot/api-client/end_to_end_example/naveenDevServiceAcc.json"

# TODO(developer)
project_id = "smart-traffic-lights-290011"
topic_id = "traffic-signals"

publisher = pubsub_v1.PublisherClient()
# The `topic_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/topics/{topic_id}`
topic_path = publisher.topic_path(project_id, topic_id)

for n in range(1, 10):
    data = "Message number {}".format(n)
    # Data must be a bytestring
    data = data.encode("utf-8")
    # When you publish a message, the client returns a future.
    future = publisher.publish(topic_path, data)
    print(future.result())

print("Published messages.")