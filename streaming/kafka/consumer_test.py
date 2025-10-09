"""
Quick consumer test to verify messages arriving on Kafka.
"""
from streaming.kafka.kafka_utils import get_consumer

consumer = get_consumer("pubmed_raw")
print("🟢 Listening for messages... (Ctrl+C to stop)")
for msg in consumer:
    print(f"📥 Received → {msg.value}")
