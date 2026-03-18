from specklepy.objects.graph_traversal.traversal import GraphTraversal
from specklepy.objects.graph_traversal.default_traversal import create_default_traversal_function

def build_applicationid_index(received_data):
    """
    Build a dictionary mapping applicationId to objects.

    Why this is needed: InstanceDefinition objects reference other
    objects by applicationId, not by direct embedding.

    Returns:
        Dictionary: {applicationId: object}
    """

    index = {}
    traversal_function = create_default_traversal_function()

    for traversal_item in traversal_function.traverse(received_data):
        obj = traversal_item.current #The current base object

        # Index any object with an applicationId
        if hasattr(obj, "applicationId") and obj.applicationId:
            index[obj.applicationId] = obj
            # print(obj.applicationId)

    return index