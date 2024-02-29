import logging
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Get Key Vault name and URI from environment variables
    key_vault_name = os.environ["KEY_VAULT_NAME"]
    key_vault_uri = f"https://{key_vault_name}.vault.azure.net"

    # Authenticate with Azure AD using DefaultAzureCredential
    credential = DefaultAzureCredential()

    # Create SecretClient instance
    client = SecretClient(vault_url=key_vault_uri, credential=credential)

    # List all certificate secrets
    certificates = []
    for secret in client.list_properties_of_secrets():
        if secret.name.endswith(".crt"):  # Filter for certificates based on extension
            certificates.append({"name": secret.name, "expiration_date": secret.properties.expires_on})

    # Convert certificates list to JSON format
    json_data = json.dumps(certificates)

    # Return response with JSON data
    return func.HttpResponse(
        body=json_data,
        status_code=200,
        content_type="application/json"
    )