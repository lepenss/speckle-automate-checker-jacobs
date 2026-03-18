from specklepy.transports.server import ServerTransport
from specklepy.api import operations
from specklepy.api.client import SpeckleClient

from helpers.speckle_object import SpeckleObject

from src.rule_processor import apply_rules_to_objects
from src.spreadsheet import read_rules_from_spreadsheet
from src.helpers import flatten_base

def validate_model(client: SpeckleClient, project_id: str, model_id: str, model_name: str, rules_directory: str = "rules/"):
    """Load model version, receive data, apply rules and create comments.

    This encapsulates the original validation flow.
    """
    transport = ServerTransport(stream_id=project_id, client=client)

    versions = client.model.get_with_versions(model_id, project_id, versions_limit=1)
    my_version = versions.versions.items[0]
    my_version_id = my_version.id
    print(f"✓ Last version: {my_version_id}")

    root_object_id = my_version.referenced_object

    # Receive the data using the object_id from the version
    received_data = operations.receive(
        obj_id=root_object_id,
        remote_transport=transport
    )

    print(f"✓ Received data!")


    ############################
    # rules from speckle model checker

    # Load rules and run validation
    grouped_rules, messages = read_rules_from_spreadsheet(f"{rules_directory}rules.csv")

    flat_list_of_objects = list(flatten_base(received_data))
    list_speckle_objects = [SpeckleObject(obj, model_id, model_name, my_version_id) for obj in flat_list_of_objects]

    apply_rules_to_objects(
        list_speckle_objects,
        grouped_rules,
        client,
        project_id,
        my_version_id,
    )

    ############################

    # unique value rules



    print("✓ Added comments")
    return received_data

def validate_project(client: SpeckleClient, project_id: str, rules_directory: str = "rules/"):
    print(f"Validating project {project_id}...")
    list_speckle_objects = []
    transport = ServerTransport(stream_id=project_id, client=client)
    models = client.model.get_models(project_id)
    for model in models.items:
        versions = client.model.get_with_versions(model.id, project_id, versions_limit=1)
        my_version = versions.versions.items[0]
        my_version_id = my_version.id

        root_object_id = my_version.referenced_object

        # Receive the data using the object_id from the version
        received_data = operations.receive(
            obj_id=root_object_id,
            remote_transport=transport
        )

        flat_list_of_objects = list(flatten_base(received_data))
        list_speckle_objects.extend([SpeckleObject(obj, model.id, model.name, my_version_id) for obj in flat_list_of_objects])

    print(f"✓ Received data for {len(list_speckle_objects)} objects across {len(models.items)} models!")

    ############################
    # rules from speckle model checker

    # Load rules and run validation
    grouped_rules, messages = read_rules_from_spreadsheet(f"{rules_directory}rules.csv")
    apply_rules_to_objects(
        list_speckle_objects,
        grouped_rules,
        client,
        project_id,
        my_version_id,
        project_wide=True,
    )