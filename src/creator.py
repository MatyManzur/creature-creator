from body_part import BodyPartType, BodyPart
import copy

class Snapshot():
    def __init__(self, selected_body_parts: dict[BodyPartType, BodyPart]):
        self.selected_body_parts: dict[BodyPartType, BodyPart] = copy.copy(selected_body_parts)

    def get_selected_body_part(self, type: BodyPartType) -> BodyPart | None:
        if type not in self.selected_body_parts:
            print(f"Body part type {type} not found")
            return None
        return self.selected_body_parts[type]

class Creator:
    _instance = None

    def __new__(cls, available_body_parts=None):
        if cls._instance is None:
            if available_body_parts is None:
                raise ValueError("available_body_parts must be provided for the first instance creation")
            cls._instance = super().__new__(cls)
            cls._instance._initialize(available_body_parts)
        return cls._instance

    def _initialize(self, available_body_parts):
        if not hasattr(self, "_initialized"):
            self.available_body_parts: dict[BodyPartType, set[BodyPart]] = available_body_parts
            self.selected_body_parts: dict[BodyPartType, BodyPart] = {
                key: list(value)[0] for key, value in available_body_parts.items()
            }
            self._initialized = True
    
    def get_available_body_parts(self, type: BodyPartType) -> set[BodyPart]:
        if type not in self.available_body_parts:
            print(f"Body part type {type} not found")
            return []
        return self.available_body_parts[type]
    
    # Esto nos devuelve las que están seleccionadas en ese momento
    def get_selected_body_part(self, type: BodyPartType) -> BodyPart | None:
        return self.selected_body_parts.get(type, None)
    
    def select_body_parts(self, body_parts: dict[BodyPartType, BodyPart]):
        for part in self.available_body_parts.keys():
            if part not in body_parts or body_parts[part] is None:
                body_parts[part] = self.get_selected_body_part(part)
        for type, part in body_parts.items():
            if type not in self.available_body_parts:
                print(f"Body part type {type} not found")
                return
            if part not in self.available_body_parts[type]:
                print(f"Body part {part} not available for type {type}")
                return
            self.selected_body_parts[type] = part
    
    def load_snapshot(self, snapshot: Snapshot):
        for type in self.available_body_parts.keys():
            self.selected_body_parts[type] = snapshot.get_selected_body_part(type)

    def generate_snapshot(self) -> Snapshot:
        return Snapshot(self.selected_body_parts)