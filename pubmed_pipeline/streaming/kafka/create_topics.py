"""
Simple script to create Kafka topics for the PubMed pipeline.
"""
from kafka.admin import KafkaAdminClient, NewTopic

def create_topic(name="pubmed_raw", partitions=1, replication_factor=1):
    admin = KafkaAdminClient(bootstrap_servers="localhost:9092")
    topic = NewTopic(name=name, num_partitions=partitions, replication_factor=replication_factor)
    try:
        admin.create_topics([topic])
        print(f"✅ Created topic: {name}")
    except Exception as e:
        print(f"⚠️  Topic creation skipped or failed: {e}")
    finally:
        admin.close()

if __name__ == "__main__":
    create_topic()
