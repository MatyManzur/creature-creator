import tkinter as tk
from body_part import BodyPartType
from creator import Creator


class Screen():

    def __init__(self, frame):
        self.frame = frame
        self.creator = Creator.get_instance()

    def update_screen(self):
        #print(f"{self.creator.get_selected_body_part(BodyPartType.HEAD)}, {self.creator.get_selected_body_part(BodyPartType.TORSO)}, {self.creator.get_selected_body_part(BodyPartType.LEGS)}, {self.creator.get_selected_body_part(BodyPartType.ACCESSORY)}")
        head_sprite = self.creator.get_selected_body_part(BodyPartType.HEAD).get_sprite()
        torso_sprite = self.creator.get_selected_body_part(BodyPartType.TORSO).get_sprite()
        legs_sprite = self.creator.get_selected_body_part(BodyPartType.LEGS).get_sprite()
        accessory_sprite = self.creator.get_selected_body_part(BodyPartType.ACCESSORY).get_sprite()

        for widget in self.frame.winfo_children():
            widget.destroy()

        canvas = tk.Canvas(self.frame, bg="lightgray")
        canvas.pack(fill=tk.BOTH, expand=True)

        y_offset = 50
        for sprite in [head_sprite, torso_sprite, legs_sprite, accessory_sprite]:
            img = sprite
            canvas.create_image(100 - img.width()/2, y_offset, anchor=tk.NW, image=img)
            y_offset += img.height()
            canvas.image = img  # Keep a reference to avoid garbage collection
