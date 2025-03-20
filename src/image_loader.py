import os
from PIL import Image, ImageTk
from body_part import BodyPartType, BodyPart, Head, Torso, Legs, Wings
from sprite import Sprite

class ImageLoader():
    def __init__(self, heads_path: str, torsos_path: str, legs_path: str, wings_path: str = None):
        self.heads_path = heads_path
        self.torsos_path = torsos_path
        self.legs_path = legs_path
        self.wings_path = wings_path
    
    def __load_from_folder(self, folder_path: str, scale: float = 1.0) -> list[Sprite]:
        sprites = []
        if folder_path == None:
            return sprites
        for filename in os.listdir(folder_path):
            if filename.endswith(".png"):
                image_path = os.path.join(folder_path, filename)
                image = Image.open(image_path)
                if scale != 1.0:
                    image = image.resize((int(image.width * scale), int(image.height * scale)), Image.ANTIALIAS)
                sprite = ImageTk.PhotoImage(image)
                sprite_name = filename.split(".")[0]
                sprites.append(Sprite(sprite_name, sprite))
        return sprites

    def load_sprites(self) -> dict[BodyPartType, list[BodyPart]]:
        sprites = {
            BodyPartType.HEAD: [Head(sprite.name, sprite.sprite, index) for index, sprite in enumerate(self.__load_from_folder(self.heads_path))],
            BodyPartType.TORSO: [Torso(sprite.name, sprite.sprite, index) for index, sprite in enumerate(self.__load_from_folder(self.torsos_path))],
            BodyPartType.LEGS: [Legs(sprite.name, sprite.sprite, index) for index, sprite in enumerate(self.__load_from_folder(self.legs_path))],
            BodyPartType.WINGS: [Wings(sprite.name, sprite.sprite, index) for index, sprite in enumerate(self.__load_from_folder(self.wings_path, 1.7))]
        }
        return sprites
