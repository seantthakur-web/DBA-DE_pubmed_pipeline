"""
Key Vault client helper for PubMed Pipeline.
Clean rebuilt version – matches repo folder structure.
"""

from utils.log_config import get_logger

logger = get_logger(__name__)

try:
    from azure.identity import DefaultAzureCredential
    from azure.keyvault.secrets import SecretClient
except ImportError:
    logger.warning("Azure SDK not installed; Key Vault features disabled.")
    DefaultAzureCredential = None
    SecretClient = None


def get_secret(secret_name: str) -> str:
    """
    Retrieve a secret from Azure Key Vault.
    If Azure SDK or credentials are unavailable, a warning is logged
    and an empty string is returned.
    """
    if SecretClient is None or DefaultAzureCredential is None:
        logger.warning("Key Vault not available — returning empty string for %s", secret_name)
        return ""

    try:
        credential = DefaultAzureCredential()
        vault_url = "https://pubmed-pipeline-kv.vault.azure.net"
        client = SecretClient(vault_url=vault_url, credential=credential)
        secret = client.get_secret(secret_name)
        return secret.value
    except Exception as exc:
        logger.warning("Failed to retrieve secret '%s': %s", secret_name, exc)
        return ""
