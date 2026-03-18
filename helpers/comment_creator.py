"""Issue creator for Speckle projects."""

from gql import gql
from specklepy.objects.base import Base
from helpers.speckle_object import SpeckleObject
from helpers import get_mesh_centroid

class CommentCreator:
    """Creates issues in Speckle projects with 3D viewer state."""

    # 1x1 transparent PNG as placeholder screenshot
    DEFAULT_SCREENSHOT = (
        "data:image/png;base64,"
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    )

    def __init__(self, client, project_id, model_id, version_id):
        """Initialize the issue creator."""
        self.client = client
        self.project_id = project_id
        self.model_id = model_id
        self.version_id = version_id
        self.resource_id_string = f"{self.model_id}@{self.version_id}"
        self.existing_comments = self._fetch_existing_comments()

    def _fetch_existing_comments(self) -> dict:
        """Fetch existing comments for the resource to avoid duplicates."""
        query = gql(
            """
	        query getComments($projectId: String!) {
                project(id: $projectId) {
                    commentThreads{
                        items{
                            rawText
                        }
                    }
                }
            }
            """
        )    

        params = {"projectId": self.project_id}
        result = self.client.httpclient.execute(query, params)

        comments = result["project"]["commentThreads"]["items"]
        existing_comments_raw_text = []
        for comment in comments:
            existing_comments_raw_text.append(comment["rawText"])

        return existing_comments_raw_text

    def create_comment_for_object(
        self,
        title: str,
        speckle_obj: SpeckleObject | list[SpeckleObject],
    ) -> dict:
        """Create an issue per object.

        Args:
            title: The issue title.
            objects: List of Speckle objects to highlight.
            description: Issue description text.
            camera_distance: Distance from centroid for camera position.

        Returns:
            The created issue data as a dictionary.
        """

        if title in self.existing_comments:
            print(f"Comment with title '{title}' already exists. Skipping creation.")
            return
        
        if not speckle_obj:
            raise ValueError("At least one object is required")

        # Build selectedObjectApplicationIds for all objects
        
        selected_object = {}
        if isinstance(speckle_obj, list):
            for speckleobj in speckle_obj:
                obj = speckleobj.object
                object_id = obj.id
                application_id = getattr(obj, "applicationId", "") or ""
                selected_object[object_id] = application_id
        else:
            object_id = speckle_obj.object.id
            application_id = getattr(speckle_obj.object, "applicationId", "") or ""
            selected_object[object_id] = application_id

        # Use first object's centroid for camera target
        if isinstance(speckle_obj, list):
            centroid = get_mesh_centroid(speckle_obj[0].object)
        else:         
            centroid = get_mesh_centroid(speckle_obj.object)
        target = [
            centroid[0],
            centroid[1] + 0.01,
            centroid[2],
        ]
        camera_position = [
            centroid[0],
            centroid[1] - 0.05,
            centroid[2] + 0.5,
        ]

        

        viewer_state = self._build_viewer_state(
            selected_objects=selected_object,
            target=list(target),
            camera_position=camera_position,
        )
        
        description = f"Failed application IDs: {object_id}"
        self._execute_mutation(title, viewer_state, description)

        print(f"Created comment for object {object_id} with title '{title}'")

        return 


    def _build_viewer_state(
        self,
        selected_objects: dict[str, str],
        target: list[float],
        camera_position: list[float],
    ) -> dict:
        """Build the viewer state for an issue."""
        return {
            "projectId": self.project_id,
            "sessionId": "",
            "viewer": {"metadata": {"filteringState": None}},
            "resources": {
                "request": {
                    "resourceIdString": self.resource_id_string,
                    "threadFilters": {
                        "includeArchived": False,
                        "loadedVersionsOnly": False,
                    },
                }
            },
            "ui": {
                "filters": {
                    "filterLogic": "all",
                    "hiddenObjectIds": [],
                    "propertyFilters": [],
                    "isolatedObjectIds": [],
                    "activeColorFilterId": None,
                    "selectedObjectApplicationIds": selected_objects,
                },
                "threads": {
                    "openThread": {
                        "isTyping": False,
                        "threadId": None,
                        "newThreadEditor": False,
                    }
                },
                "camera": {
                    "zoom": 1,
                    "target": target,
                    "position": camera_position,
                    "isOrthoProjection": False,
                },
                "sectionBox": None,
                "spotlightUserSessionId": None,
                "explodeFactor": 0,
            },
        }

    def _build_description_doc(self, text: str) -> dict:
        """Build the description document structure."""
        return {
            "type": "doc",
            "content": [
                {
                    "type": "paragraph",
                    "content": [{"type": "text", "text": text}],
                }
            ],
        }

    def _execute_mutation(
        self, title: str, viewer_state: dict, description: str = ""
    ) -> dict:
        """Execute the GraphQL mutation to create an issue."""

        query = gql(
            """
            mutation create($input: CreateCommentInput!) {
                commentMutations {
                    create(input: $input) {
                        id
                    }
                }
            }
            """
        )

        params = {
            "input": {
                "projectId": self.project_id,
                "resourceIdString": self.resource_id_string,
                "viewerState": viewer_state,
                "screenshot": self.DEFAULT_SCREENSHOT,
                "content":{
                    "doc": {
                        "type": "doc",
                        "content": [{
                            "type": "paragraph",
                            "content": [{
                                "type": "text",
                                "text": title,
                            }]
                        }]
                    },
                    "blobIds":[]
                }
            }
        }

        result = self.client.httpclient.execute(query, params)

        return
