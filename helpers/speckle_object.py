from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class SpeckleObject:
	"""Simple container for a Speckle object and its model id.

	Attributes:
		object: The raw speckle object (kept as Any to allow flexibility).
		model_id: Optional string id linking the object to a model.
		model_name: Optional string name linking the object to a model.
		version_id: Optional string id linking the object to a version.
	"""
	object: Any
	model_id: Optional[str] = None
	model_name: Optional[str] = None
	version_id: Optional[str] = None
	message: Optional[str] = ""

	def to_dict(self) -> dict:
		"""Return a plain dict representation."""
		return {"object": self.object, "model_id": self.model_id, "model_name": self.model_name, "version_id": self.version_id, "message": self.message}

	@staticmethod
	def from_dict(d: dict) -> "SpeckleObject":
		"""Create a SpeckleObject from a dict with keys 'object' and 'model_id'."""
		return SpeckleObject(object=d.get("object"), model_id=d.get("model_id"), model_name=d.get("model_name"), version_id=d.get("version_id"), message=d.get("message"))

