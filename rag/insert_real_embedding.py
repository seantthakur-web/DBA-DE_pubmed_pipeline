import os, requests, psycopg2
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# --- Retrieve secrets from Azure Key Vault ---
VAULT_URL = "https://pubmed-kv.vault.azure.net/"
credential = DefaultAzureCredential()
client = SecretClient(vault_url=VAULT_URL, credential=credential)

OPENAI_ENDPOINT = client.get_secret("AZURE-OPENAI-ENDPOINT").value
OPENAI_KEY = client.get_secret("AZURE-OPENAI-KEY").value
POSTGRES_CONN = client.get_secret("POSTGRES-CONN").value

# --- Generate embedding for a sample sentence ---
text = "Cisplatin and S-1 improve survival in advanced gastric cancer."

url = f"{OPENAI_ENDPOINT}openai/deployments/text-embedding-ada-002/embeddings?api-version=2023-05-15"
headers = {"Content-Type": "application/json", "api-key": OPENAI_KEY}
payload = {"input": text}

r = requests.post(url, headers=headers, json=payload)
r.raise_for_status()
embedding = r.json()["data"][0]["embedding"]

# --- Insert into Postgres ---
conn = psycopg2.connect(POSTGRES_CONN)
cur = conn.cursor()
cur.execute("""
    INSERT INTO pubmed_embeddings (doc_id, content, embedding)
    VALUES (%s, %s, %s)
""", ("PMID_REAL_EMB", text, embedding))
conn.commit()
cur.close()
conn.close()

print("✅ Inserted real embedding successfully!")
