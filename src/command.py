from body_part import Head, Torso, Legs, Accessory, BodyPartType
from creator import Creator, VersionManager
from typing import Optional
from abc import ABC, abstractmethod

class BaseCommand(ABC):
    @abstractmethod
    def execute(self):
        pass

class NewVersionCommand(BaseCommand):
    def __init__(self, head: Optional[Head], torso: Optional[Torso], legs: Optional[Legs], accessory: Optional[Accessory]):
        self.head = head
        self.torso = torso
        self.legs = legs
        self.accessory = accessory

    def execute(self):
        VersionManager.get_instance().save_snapshot()
        Creator.get_instance().select_body_parts({
            BodyPartType.HEAD: self.head,
            BodyPartType.TORSO: self.torso,
            BodyPartType.LEGS: self.legs,
            BodyPartType.ACCESSORY: self.accessory
        })

class NewVersionCommandBuilder:
    _instance = None

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
            self.accessory = None
            self._initialized = True

    def reset(self):
        self.head = None
        self.torso = None
        self.legs = None
        self.accessory = None
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

    def set_accessory(self, accessory: Accessory):
        self.accessory = accessory
        return self

    def build(self) -> NewVersionCommand:
        command = NewVersionCommand(self.head, self.torso, self.legs, self.accessory)
        return command

class UndoCommand(BaseCommand):
    def __init__(self):
        super().__init__()
    
    def execute(self):
        VersionManager.get_instance().undo()

class RedoCommand(BaseCommand):
    def __init__(self):
        super().__init__()
    
    def execute(self):
        VersionManager.get_instance().redo()



