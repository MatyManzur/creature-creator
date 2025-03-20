import tkinter as tk
from tkinter import ttk
from body_part import BodyPartType
from window_config import prepare_window
from image_loader import ImageLoader
from command import UndoCommand, RedoCommand, generate_random_command, generate_simple_command
from creator import Creator
from screen import Screen


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

    footer = tk.Frame(root, width=400, height=20)
    footer.grid(row=1, column=0, sticky="ew")

    # Left section with images
    left_frame = tk.Frame(main_frame, width=200, height=200, bg="lightgray")
    left_frame.pack(side=tk.LEFT, fill=tk.Y)
    left_frame.pack_propagate(False)  # Prevents auto-resizing

    # Right section with checkboxes
    right_frame = tk.Frame(main_frame, width=200, height=200, bg="white")
    right_frame.pack(side=tk.RIGHT, fill=tk.Y)
    right_frame.pack_propagate(False)  # Prevents auto-resizing

    screen: Screen = Screen(left_frame)
    creator.subscribe_callback(screen.update_screen)

    #ttk.Label(right_frame, text="Options").grid(row=0, column=0, columnspan=4, pady=10)


    row_index = 1
    max_per_row = 4
    vars = {}
    for value in BodyPartType.__members__.keys():
        ttk.Label(right_frame, text=value).grid(row=row_index, column=0, padx=10, pady=5, sticky="w")
        vars[value] = (tk.IntVar())
        body_parts = creator.get_available_body_parts(BodyPartType[value])

        for i in range(len(body_parts)):  
            col_index = (i % max_per_row) + 1  
            row_offset = i // max_per_row  
            radiobutton = ttk.Radiobutton(right_frame, text=f"{body_parts[i].get_name()}", variable=vars[value], value=body_parts[i].get_index(),
                                          command=lambda curr_body_part=body_parts, v=value: generate_simple_command(curr_body_part[vars[v].get()]))
            radiobutton.grid(row=row_index + row_offset, column=col_index, padx=5, pady=5, sticky="w")
        vars[value].set(0)
        
        separator = ttk.Separator(right_frame, orient='horizontal')
        separator.grid(row=row_index + (6 // max_per_row), column=0, columnspan=5, sticky="ew")
        row_index += (6 // max_per_row) + 1 

    def update_vars():
        creator = Creator.get_instance()
        body_parts = {
            BodyPartType.HEAD,
            BodyPartType.TORSO,
            BodyPartType.LEGS,
            BodyPartType.WINGS,
        }
        for part_type in body_parts:
            vars[part_type.name].set(creator.get_selected_body_part(part_type).get_index())

    def random_command_with_vars_update(*args):
        generate_random_command()
        update_vars()

    def undo_command_with_vars_update(*args):
        UndoCommand().execute()
        update_vars()

    def redo_command_with_vars_update(*args):
        RedoCommand().execute()
        update_vars()


    dice_icon = tk.PhotoImage(file='./src/assets/button_icons/dice.png').subsample(80,80)
    random_button = ttk.Button(right_frame, text="Random", command=random_command_with_vars_update, image=dice_icon)
    random_button.grid(row=0, column=0, padx=10, pady=10, sticky="e")
    go_back_icon = tk.PhotoImage(file='./src/assets/button_icons/go_back.png').subsample(65,65)
    go_back_button = ttk.Button(right_frame, text="Undo", command=undo_command_with_vars_update, image=go_back_icon)
    go_back_button.grid(row=0, column=3, padx=0, pady=10, sticky="e")
    go_forward_icon = tk.PhotoImage(file='./src/assets/button_icons/go_forward.png').subsample(65,65)
    go_forward_button = ttk.Button(right_frame, text="Redo", command=redo_command_with_vars_update, image=go_forward_icon)
    go_forward_button.grid(row=0, column=4, padx=10, pady=10, sticky="e")

    root.bind("<Control-z>", undo_command_with_vars_update)
    root.bind("<Control-y>", redo_command_with_vars_update)
    root.bind("<Control-r>", random_command_with_vars_update)

    footer_label = ttk.Label(footer, text="Ctrl+Z: Undo | Ctrl+Y: Redo | Ctrl+R: Randomize")
    footer_label.pack(side=tk.LEFT, padx=10)

    root.mainloop()

if __name__ == "__main__":
    main()