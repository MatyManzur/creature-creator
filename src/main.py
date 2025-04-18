import tkinter as tk
from image_loader import ImageLoader
from creator import Creator
from screen import CreatureScreen, prepare_footer, prepare_options_panel, prepare_story_panels, prepare_window
from async_tkinter_loop import async_mainloop
import yaml

CONFIG_FILE = "config.yaml"
with open(CONFIG_FILE, "r") as file:
    config = yaml.safe_load(file)
    MODELS = config.get("available_models", ["llama3.2:1b"])


def main():
    root = tk.Tk()

    prepare_window(root)

    image_loader: ImageLoader = ImageLoader(
        heads_path="./src/assets/body_parts/heads/",
        torsos_path="./src/assets/body_parts/torsos/",
        legs_path="./src/assets/body_parts/legs/",
        wings_path="./src/assets/body_parts/wings/"
    )

    creator: Creator = Creator.get_instance(image_loader.load_sprites())

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Create a main frame to hold the two sections
    main_frame = tk.Frame(root, width=400, height=200)
    main_frame.grid(row=0, column=0, sticky="nsew")

    # Everything related to the story
    prepare_story_panels(root, creator, MODELS)
    
    footer = tk.Frame(root, width=400, height=20)
    footer.grid(row=1, column=0, sticky="ew")

    # Left section with the creature
    left_frame = tk.Frame(main_frame, width=200, height=200, bg="lightgray")
    left_frame.pack(side=tk.LEFT, fill=tk.Y)
    left_frame.pack_propagate(False)  # Prevents auto-resizing

    # Right section with checkboxes
    right_frame = tk.Frame(main_frame, width=200, height=200, bg="white")
    right_frame.pack(side=tk.RIGHT, fill=tk.Y)
    right_frame.pack_propagate(False)  # Prevents auto-resizing

    creature_screen: CreatureScreen = CreatureScreen(left_frame)
    creator.subscribe_callback(creature_screen.update_screen)    

    prepare_options_panel(root, right_frame, creator)

    prepare_footer(footer)

    async_mainloop(root)
     

if __name__ == "__main__":
    main()