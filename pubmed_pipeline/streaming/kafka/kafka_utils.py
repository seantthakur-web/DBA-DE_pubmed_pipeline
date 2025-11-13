"""
Common Kafka utilities: producer and consumer builders.
"""
from kafka import KafkaProducer, KafkaConsumer
import json

def get_producer(bootstrap_servers: str = "localhost:9092"):
    """Create and return a Kafka producer."""
    return KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

def get_consumer(topic: str, bootstrap_servers: str = "localhost:9092", group_id: str = "pubmed-group"):
    """Create and return a Kafka consumer."""
    return KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id=group_id,
        auto_offset_reset="earliest",
        value_deserializer=lambda m: json.loads(m.decode("utf-8"))
    )
