from PIL import ImageTk

class Sprite():
    def __init__(self, name: str, sprite: ImageTk.PhotoImage):
        self.name = name
        self.sprite = sprite