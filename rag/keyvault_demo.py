from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

VAULT_URL = "https://pubmed-kv.vault.azure.net/"
credential = DefaultAzureCredential()
client = SecretClient(vault_url=VAULT_URL, credential=credential)

for name in ["AZURE-OPENAI-ENDPOINT", "AZURE-OPENAI-KEY", "POSTGRES-CONN", "SERVICEBUS-CONN"]:
    secret = client.get_secret(name)
    print(f"{name}: {secret.value[:40]}...")
