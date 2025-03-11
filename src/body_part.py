import abc
from enum import Enum
from abc import ABC

class BodyPartType(Enum):
    HEAD = 1,
    TORSO = 2,
    LEGS = 3,
    ACCESSORY = 4

class BodyPart(ABC):
    def __init__(self, name: str, body_part_type: BodyPartType):
        self.name = name
        self.body_part_type = body_part_type

    def get_name(self):
        return self.name
    
    def get_body_part_type(self):
        return self.body_part_type

    @abc.abstractmethod
    def get_sprite(self):
        pass

class Head(BodyPart):
    def __init__(self, name: str):
        super().__init__(name, BodyPartType.HEAD)

class Torso(BodyPart):
    def __init__(self, name: str):
        super().__init__(name, BodyPartType.TORSO)

class Legs(BodyPart):
    def __init__(self, name: str):
        super().__init__(name, BodyPartType.LEGS)

class Accessory(BodyPart):
    def __init__(self, name: str):
        super().__init__(name, BodyPartType.ACCESSORY)
