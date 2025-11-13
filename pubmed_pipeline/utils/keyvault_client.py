
import logging
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from utils.log_config import get_logger

logger = get_logger("keyvault_client")


def get_secret(secret_name: str, keyvault_url: str = None) -> str:
    """
    Retrieves a secret from Azure Key Vault.
    For local development, ensure AZURE_TENANT_ID, AZURE_CLIENT_ID, 
    and AZURE_CLIENT_SECRET are exported.
    """

    if not keyvault_url:
        raise ValueError("Key Vault URL must be provided")

    try:
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=keyvault_url, credential=credential)

        logger.info(f"Retrieving secret '{secret_name}' from Key Vault...")
        secret = client.get_secret(secret_name)
        return secret.value

    except Exception as e:
        logger.error(f"Failed to retrieve secret '{secret_name}': {e}")
        raise
