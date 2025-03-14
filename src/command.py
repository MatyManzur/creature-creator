from body_part import Head, Torso, Legs, Accessory, BodyPartType
from creator import Creator
from typing import Optional

class Command():
    def __init__(self, head: Optional[Head], torso: Optional[Torso], legs: Optional[Legs], accessory: Optional[Accessory]):
        self.head = head
        self.torso = torso
        self.legs = legs
        self.accessory = accessory

    def __str__(self):
        return self.head.get_name() + " " + self.torso.get_name() + " " + self.legs.get_name() + " " + self.accessory.get_name()

    def execute(self):
        Creator().select_body_parts({
            BodyPartType.HEAD: self.head,
            BodyPartType.TORSO: self.torso,
            BodyPartType.LEGS: self.legs,
            BodyPartType.ACCESSORY: self.accessory
        })


class CommandBuilder:
    _instance = None

    @staticmethod
    def get_instance():
        if CommandBuilder._instance is None:
            CommandBuilder._instance = CommandBuilder()
        return CommandBuilder._instance

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

    def build(self) -> Command:
        command = Command(self.head, self.torso, self.legs, self.accessory)
        return command





