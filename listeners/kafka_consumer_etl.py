import os, json, time
from azure.servicebus import ServiceBusClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.getcwd(), "configs/.env"))

connection_str = os.getenv("SERVICE_BUS_CONNECTION_STR")
topic_name = os.getenv("SERVICE_BUS_TOPIC_NAME")
subscription_name = os.getenv("SERVICE_BUS_SUBSCRIPTION_NAME")

with ServiceBusClient.from_connection_string(connection_str) as client:
    receiver = client.get_subscription_receiver(topic_name, subscription_name)
    with receiver:
        print(f"🔁 Listening on topic '{topic_name}' / subscription '{subscription_name}' ...")
        for msg in receiver:
            body = str(msg)
            try:
                data = json.loads(body)
            except Exception:
                data = {"raw": body}
            print(f"📥 Received message:\n{json.dumps(data, indent=2)}\n")
            receiver.complete_message(msg)
            break  # stop after first message for test
print("✅ Consumer finished.")
