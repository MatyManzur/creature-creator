import abc
from enum import Enum
from abc import ABC
from sprite import Sprite

class BodyPartType(Enum):
    HEAD = 1,
    TORSO = 2,
    LEGS = 3,
    ACCESSORY = 4

class BodyPart(ABC):
    def __init__(self, name: str, body_part_type: BodyPartType, sprite: Sprite):
        self.name = name
        self.body_part_type = body_part_type
        self.sprite = sprite

    def get_name(self):
        return self.name
    
    def get_body_part_type(self):
        return self.body_part_type

    def get_sprite(self):
        return self.sprite
    
    def __str__(self):
        return self.name
    
    def __eq__(self, value):
        return self.name == value.name and self.body_part_type == value.body_part_type
    
    def __hash__(self):
        return hash((self.name, self.body_part_type))

class Head(BodyPart):
    def __init__(self, name: str, sprite: Sprite):
        super().__init__(name, BodyPartType.HEAD, sprite)

class Torso(BodyPart):
    def __init__(self, name: str, sprite: Sprite):
        super().__init__(name, BodyPartType.TORSO, sprite)

class Legs(BodyPart):
    def __init__(self, name: str, sprite: Sprite):
        super().__init__(name, BodyPartType.LEGS, sprite)

class Accessory(BodyPart):
    def __init__(self, name: str, sprite: Sprite):
        super().__init__(name, BodyPartType.ACCESSORY, sprite)
