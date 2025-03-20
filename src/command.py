import random
from body_part import BodyPart, Head, Torso, Legs, Wings, BodyPartType
from creator import Creator, VersionManager
from typing import Optional
from abc import ABC, abstractmethod

class BaseCommand(ABC):
    @abstractmethod
    def execute(self):
        pass

# Command pattern
class NewVersionCommand(BaseCommand):
    def __init__(self, head: Optional[Head], torso: Optional[Torso], legs: Optional[Legs], wings: Optional[Wings]):
        self.head = head
        self.torso = torso
        self.legs = legs
        self.wings = wings

    def execute(self):
        VersionManager.get_instance().save_snapshot()
        Creator.get_instance().select_body_parts({
            BodyPartType.HEAD: self.head,
            BodyPartType.TORSO: self.torso,
            BodyPartType.LEGS: self.legs,
            BodyPartType.WINGS: self.wings
        })

# Builder pattern, as an extra!
class NewVersionCommandBuilder:
    _instance = None

    # Singleton pattern
    @staticmethod
    def get_instance():
        if NewVersionCommandBuilder._instance is None:
            NewVersionCommandBuilder._instance = NewVersionCommandBuilder()
        return NewVersionCommandBuilder._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):  
            self.head = None
            self.torso = None
            self.legs = None
            self.wings = None
            self._initialized = True

    def reset(self):
        self.head = None
        self.torso = None
        self.legs = None
        self.wings = None
        return self

    def set_head(self, head: Head):
        self.head = head
        return self

    def set_torso(self, torso: Torso):
        self.torso = torso
        return self

    def set_legs(self, legs: Legs):
        self.legs = legs
        return self

    def set_wings(self, wings: Wings):
        self.wings = wings
        return self

    def build(self) -> NewVersionCommand:
        command = NewVersionCommand(self.head, self.torso, self.legs, self.wings)
        return command

# Command pattern
class UndoCommand(BaseCommand):
    def __init__(self):
        super().__init__()
    
    def execute(self):
        VersionManager.get_instance().undo()

# Command pattern
class RedoCommand(BaseCommand):
    def __init__(self):
        super().__init__()
    
    def execute(self):
        VersionManager.get_instance().redo()

# Command pattern
def generate_random_command():
    creator = Creator.get_instance()
    body_parts = creator.get_available_body_parts(BodyPartType.HEAD)
    head = body_parts[random.randint(0, len(creator.get_available_body_parts(BodyPartType.HEAD)) - 1)]
    body_parts = creator.get_available_body_parts(BodyPartType.TORSO)
    torso = body_parts[random.randint(0, len(creator.get_available_body_parts(BodyPartType.TORSO)) - 1)]
    body_parts = creator.get_available_body_parts(BodyPartType.LEGS)
    legs = body_parts[random.randint(0, len(creator.get_available_body_parts(BodyPartType.LEGS)) - 1)]
    body_parts = creator.get_available_body_parts(BodyPartType.WINGS)
    wings = body_parts[random.randint(0, len(creator.get_available_body_parts(BodyPartType.WINGS)) - 1)]
    NewVersionCommandBuilder.get_instance().set_head(head).set_torso(torso).set_legs(legs).set_wings(wings).build().execute()
    NewVersionCommandBuilder.get_instance().reset()


builder_methods = {
    BodyPartType.HEAD: NewVersionCommandBuilder.get_instance().set_head,
    BodyPartType.TORSO: NewVersionCommandBuilder.get_instance().set_torso,
    BodyPartType.LEGS: NewVersionCommandBuilder.get_instance().set_legs,
    BodyPartType.WINGS: NewVersionCommandBuilder.get_instance().set_wings,
}

def generate_simple_command(body_part: BodyPart):
    type: BodyPartType = body_part.get_body_part_type()
    builder = NewVersionCommandBuilder.get_instance()
    builder_methods[type](body_part)
    builder.build().execute()
    NewVersionCommandBuilder.get_instance().reset()



