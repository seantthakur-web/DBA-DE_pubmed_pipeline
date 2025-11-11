import os, json, psycopg2
from azure.servicebus import ServiceBusClient
from openai import AzureOpenAI
from dotenv import load_dotenv
import numpy as np

# --- Load configuration ---
load_dotenv(os.path.join(os.getcwd(), "configs/.env"))

sb_conn  = os.getenv("SERVICE_BUS_CONNECTION_STR")
topic    = os.getenv("SERVICE_BUS_TOPIC_NAME")
sub      = os.getenv("SERVICE_BUS_SUBSCRIPTION_NAME")

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key  = os.getenv("AZURE_OPENAI_API_KEY")
deploy   = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")

pg_conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    sslmode="require"
)
cursor = pg_conn.cursor()

client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version="2024-02-15-preview"
)

# --- Consume Service Bus messages ---
with ServiceBusClient.from_connection_string(sb_conn) as sb_client:
    receiver = sb_client.get_subscription_receiver(topic, sub)
    with receiver:
        print(f"🔁 Listening on topic '{topic}' → Azure AI Embeddings → PostgreSQL(pubmed_vectors)")
        for msg in receiver:
            try:
                body = json.loads(str(msg))
            except json.JSONDecodeError:
                print("⚠️ Message skipped — not valid JSON")
                receiver.complete_message(msg)
                continue

            pmid = str(body.get("pmid") or body.get("id") or "unknown")
            title = body.get("title", "")
            abstract = body.get("abstract", "")

            text = f"{title}\n\n{abstract}"
            if not abstract:
                print(f"⚠️ Missing abstract for PMID {pmid}, skipping")
                receiver.complete_message(msg)
                continue

            print(f"🧠 Embedding PMID {pmid}: {title[:60]}...")

            # Generate embedding via Azure AI
            emb = client.embeddings.create(model=deploy, input=text)
            vector = np.array(emb.data[0].embedding, dtype=np.float32)

            # Upsert into Postgres
            cursor.execute("""
                INSERT INTO pubmed_vectors (pmid, title, abstract, embedding)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (pmid) DO UPDATE
                SET title = EXCLUDED.title,
                    abstract = EXCLUDED.abstract,
                    embedding = EXCLUDED.embedding;
            """, (pmid, title, abstract, vector.tolist()))
            pg_conn.commit()

            receiver.complete_message(msg)
            print(f"✅ Stored / updated embedding for PMID {pmid}\n")

        print("🔚 Listener finished (processed available messages)")

cursor.close()
pg_conn.close()
