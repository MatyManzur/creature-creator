import os
import tkinter as tk
from PIL import Image, ImageTk
from .body_part import BodyPartType
from .sprite import Sprite

class ImageLoader():
    def __init__(self, heads_path: str, torsos_path: str, legs_path: str, accessories_path: str):
        self.heads_path = heads_path
        self.torsos_path = torsos_path
        self.legs_path = legs_path
        self.accessories_path = accessories_path
    
    def __load_from_folder(self, folder_path: str) -> list[Sprite]:
        sprites = []
        for filename in os.listdir(folder_path):
            if filename.endswith(".png"):
                image_path = os.path.join(folder_path, filename)
                image = Image.open(image_path)
                sprite = ImageTk.PhotoImage(image)
                sprite_name = filename.split(".")[0]
                sprites.append(Sprite(sprite_name, sprite))
        return sprites

    def load_sprites(self) -> dict[BodyPartType, list[Sprite]]:
        sprites = {
            BodyPartType.HEAD: self.__load_from_folder(self.heads_path),
            BodyPartType.TORSO: self.__load_from_folder(self.torsos_path),
            BodyPartType.LEGS: self.__load_from_folder(self.legs_path),
            BodyPartType.ACCESSORY: self.__load_from_folder(self.accessories_path)
        }
        return sprites
