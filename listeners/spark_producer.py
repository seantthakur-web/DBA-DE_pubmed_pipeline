import os, json, time
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.getcwd(), "configs/.env"))

# --- Service Bus Config ---
connection_str = os.getenv("SERVICE_BUS_CONNECTION_STR")
topic_name = os.getenv("SERVICE_BUS_TOPIC_NAME")

# --- Mock PubMed Record ---
message = {
    "pmid": "2055453",
    "title": "Phase III FLAGS Trial: Cisplatin and S-1 vs Cisplatin and 5-FU",
    "abstract": (
        "The FLAGS study compared the efficacy and safety of cisplatin/S-1 "
        "versus cisplatin/5-FU in patients with advanced gastric or "
        "gastroesophageal adenocarcinoma. Results showed comparable efficacy "
        "and improved tolerability in the S-1 arm."
    ),
    "timestamp": time.time()
}

# --- Send to Service Bus ---
with ServiceBusClient.from_connection_string(connection_str) as client:
    sender = client.get_topic_sender(topic_name)
    with sender:
        sender.send_messages(ServiceBusMessage(json.dumps(message)))
        print(f"✅ Sent PubMed record {message['pmid']} to topic: {topic_name}")
