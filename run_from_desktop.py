
# Disable logging
import logging
logging.getLogger("specklepy.logging.metrics").disabled = True
from specklepy.logging import metrics
metrics.disable()

from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_local_accounts

from helpers.validation import validate_model, validate_project

print("✓ specklepy installed successfully!")

SPECKLE_SERVER_URL = "ldd-emea.jacobs.com"

# Default project and model identifiers (can be parameterized)
project_id = '354a8c26b8'
# model_id = 'c1135ffebc'


def speckle_authenticate(server_url: str = SPECKLE_SERVER_URL):
    """Authenticate a Speckle client using local desktop accounts.

    Returns an authenticated `SpeckleClient` instance.
    """
    client = SpeckleClient(host=server_url)
    accounts = get_local_accounts()
    account = None
    for acc in accounts:
        if server_url in acc.serverInfo.url:
            account = acc
            break
    if account is None:
        raise RuntimeError(f"No local account found for {server_url}")

    client.authenticate_with_account(account)
    print(f"✓ Authenticated as {client.account.userInfo.name} to {client.url}")
    return client


if __name__ == "__main__":
    client = speckle_authenticate()
    validate_project(client, project_id, rules_directory="rules/rules_MSD/")
    models = client.model.get_models(project_id)
    for model in models.items:
        print(f"Validating model: {model.name}")
        validate_model(client, project_id, model.id, model.name, rules_directory="rules/rules_MSD/")