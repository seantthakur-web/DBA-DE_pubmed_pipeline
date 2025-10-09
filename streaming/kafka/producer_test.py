"""
Quick test producer that sends sample PubMed messages to Kafka.
"""
from streaming.kafka.kafka_utils import get_producer
import time

producer = get_producer()

for i in range(3):
    msg = {"pmid": f"TEST_{i}", "xml": "<PubMed>Sample</PubMed>"}
    producer.send("pubmed_raw", msg)
    print(f"📤 Sent {msg['pmid']}")
    time.sleep(1)

producer.flush()
print("✅ Producer test complete.")
