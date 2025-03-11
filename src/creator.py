from .body_part import BodyPartType, BodyPart
import copy

class Snapshot():
    def __init__(self, selected_body_parts: dict[BodyPartType, int]):
        self.selected_body_parts: dict[BodyPartType, int] = copy.copy(selected_body_parts)

    def get_selected_body_part_index(self, type: BodyPartType) -> int | None:
        if type not in self.selected_body_parts:
            print(f"Body part type {type} not found")
            return None
        return self.selected_body_parts[type]

class Creator():
    def __init__(self, available_body_parts: dict[BodyPartType, list[BodyPart]]):
        self.available_body_parts: dict[BodyPartType, list[BodyPart]] = available_body_parts
        initial_selected_body_parts: dict[BodyPartType, int] = {
            type: 0 for type in available_body_parts.keys() if len(available_body_parts[type]) > 0
        }
        self.snapshots: list[Snapshot] = [
            Snapshot(initial_selected_body_parts)
        ]
    
    def get_available_body_parts(self, type: BodyPartType) -> list[BodyPart]:
        if type not in self.available_body_parts:
            print(f"Body part type {type} not found")
            return []
        return self.available_body_parts[type]
    
    def get_selected_body_part(self, type: BodyPartType) -> BodyPart | None:
        snapshot: Snapshot = self.snapshots[-1]
        return self.available_body_parts[type][snapshot.get_selected_body_part_index(type)]
    
    def select_body_parts(self, body_parts: dict[BodyPartType, int]):
        snapshot: Snapshot = self.snapshots[-1]
        for part in self.available_body_parts.keys():
            if part not in body_parts:
                body_parts[part] = snapshot.get_selected_body_part_index(part)
            else:
                if part not in self.available_body_parts:
                    print(f"Body part type {part} not found")
                    return
                body_parts[part] = body_parts[part] % len(self.available_body_parts[part])
        self.snapshots.append(Snapshot(body_parts))