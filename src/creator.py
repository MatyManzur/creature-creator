from body_part import BodyPartType, BodyPart
import copy

# Used for the Memento pattern
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

    # Singleton pattern
    @staticmethod
    def get_instance(available_body_parts=None):
        if Creator._instance is None:
            if available_body_parts is None:
                raise ValueError("available_body_parts must be provided for the first instance creation")
            Creator._instance = Creator.__new__(Creator)
            Creator._instance._initialize(available_body_parts) 
        return Creator._instance

    def _initialize(self, available_body_parts):
        if not hasattr(self, "_initialized"):  # Prevent re-initialization
            self.available_body_parts: dict[BodyPartType, set[BodyPart]] = available_body_parts
            self.selected_body_parts: dict[BodyPartType, BodyPart] = {
                key: list(value)[0] for key, value in available_body_parts.items()
            }
            self.callbacks: list[callable] = []
            self._initialized = True
    
    def get_available_body_parts(self, type: BodyPartType) -> set[BodyPart]:
        if type not in self.available_body_parts:
            print(f"Body part type {type} not found")
            return []
        return self.available_body_parts[type]
    
    def subscribe_callback(self, callback: callable):
        self.callbacks.append(callback)
        callback()
    
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
        for callback in self.callbacks:
            callback()
    
    # Memento pattern
    def load_snapshot(self, snapshot: Snapshot):
        for type in self.available_body_parts.keys():
            self.selected_body_parts[type] = snapshot.get_selected_body_part(type)
        for callback in self.callbacks:
            callback()

    # Memento pattern
    def generate_snapshot(self) -> Snapshot:
        return Snapshot(self.selected_body_parts)
    

class VersionManager():
    _instance = None

    # Singleton pattern
    @staticmethod
    def get_instance():
        if VersionManager._instance is None:
            VersionManager._instance = VersionManager()
        return VersionManager._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):  
            self._initialized = True
            self.__prev_snapshots = []
            self.__next_snapshots = []
            
    def save_snapshot(self):
        self.__prev_snapshots.append(Creator.get_instance().generate_snapshot())
        self.__next_snapshots = []
    
    def undo(self):
        if len(self.__prev_snapshots) == 0:
            print("No more snapshots to undo")
            return
        current_snapshot = self.__prev_snapshots.pop()
        self.__next_snapshots.append(Creator.get_instance().generate_snapshot())
        Creator.get_instance().load_snapshot(current_snapshot)

    def redo(self):
        if len(self.__next_snapshots) == 0:
            print("No more snapshots to redo")
            return
        current_snapshot = self.__next_snapshots.pop()
        self.__prev_snapshots.append(Creator.get_instance().generate_snapshot())
        Creator.get_instance().load_snapshot(current_snapshot)