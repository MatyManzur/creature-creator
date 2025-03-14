import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from body_part import BodyPartType
from window_config import ChangeMe, go_back, prepare_window, show_message
from creator import Creator
from image_loader import ImageLoader


def show_selected_body_parts(vars, left_frame):
    selected_body_parts = {BodyPartType[key]: vars[key].get() for key in vars.keys()}
    creator.select_body_parts(selected_body_parts)
    print(f"{creator.get_selected_body_part(BodyPartType.HEAD)}, {creator.get_selected_body_part(BodyPartType.TORSO)}, {creator.get_selected_body_part(BodyPartType.LEGS)}, {creator.get_selected_body_part(BodyPartType.ACCESSORY)}")
    head_sprite = creator.get_selected_body_part(BodyPartType.HEAD).get_sprite()
    torso_sprite = creator.get_selected_body_part(BodyPartType.TORSO).get_sprite()
    legs_sprite = creator.get_selected_body_part(BodyPartType.LEGS).get_sprite()
    accessory_sprite = creator.get_selected_body_part(BodyPartType.ACCESSORY).get_sprite()
    # Clear the left frame
    for widget in left_frame.winfo_children():
        widget.destroy()

    # Create a canvas to hold the sprites
    canvas = tk.Canvas(left_frame, bg="lightgray")
    canvas.pack(fill=tk.BOTH, expand=True)

    # Add the sprites to the canvas
    y_offset = 50
    for sprite in [head_sprite, torso_sprite, legs_sprite, accessory_sprite]:
        img = sprite
        canvas.create_image(100 - img.width()/2, y_offset, anchor=tk.NW, image=img)
        y_offset += img.height()
        canvas.image = img  # Keep a reference to avoid garbage collection



root = tk.Tk()
prepare_window(root)

image_loader: ImageLoader = ImageLoader(
    heads_path="./src/assets/body_parts/heads/",
    torsos_path="./src/assets/body_parts/torsos/",
    legs_path="./src/assets/body_parts/legs/",
    accessories_path="./src/assets/body_parts/heads/"
)

creator: Creator = Creator(image_loader.load_sprites())

# Create a main frame to hold the two sections
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Set up the main frame
main_frame = tk.Frame(root, width=400, height=200)
main_frame.pack(fill=tk.BOTH, expand=True)

# Left section with images
left_frame = tk.Frame(main_frame, width=200, height=200, bg="lightgray")
left_frame.pack(side=tk.LEFT, fill=tk.Y)
left_frame.pack_propagate(False)  # Prevents auto-resizing

# Right section with checkboxes
right_frame = tk.Frame(main_frame, width=200, height=200, bg="white")
right_frame.pack(side=tk.RIGHT, fill=tk.Y)
right_frame.pack_propagate(False)  # Prevents auto-resizing


ttk.Label(right_frame, text="Options").grid(row=0, column=0, columnspan=4, pady=10)
go_back_icon = tk.PhotoImage(file='./src/assets/button_icons/go_back.png').subsample(65,65)
go_back_button = ttk.Button(right_frame, text="Back", command=go_back, image=go_back_icon)
go_back_button.grid(row=0, column=3, padx=40, pady=10, sticky="e")
go_forward_icon = tk.PhotoImage(file='./src/assets/button_icons/go_forward.png').subsample(65,65)
go_forward_button = ttk.Button(right_frame, text="Forward", command=go_back, image=go_forward_icon)
go_forward_button.grid(row=0, column=3, pady=10, sticky="e")

row_index = 1
max_per_row = 3
vars = {}
for value in BodyPartType.__members__.keys():
    ttk.Label(right_frame, text=value).grid(row=row_index, column=0, padx=10, pady=5, sticky="w")
    vars[value] = (tk.IntVar())
    body_parts = creator.get_available_body_parts(BodyPartType[value])

    for i in range(len(body_parts)):  
        col_index = (i % max_per_row) + 1  
        row_offset = i // max_per_row  
        radiobutton = ttk.Radiobutton(right_frame, text=f"{body_parts[i].get_name()}", variable=vars[value], value=i)
        radiobutton.grid(row=row_index + row_offset, column=col_index, padx=5, pady=5)
    # Esto es para que se llame a la función aunque cambies el valor del radiobutton de una manera distinta clickearlo, 
    # si solo querés que se llame cuando clickeás, sacá el trace_add y poné el command en el radiobutton
    vars[value].trace_add("write", lambda *args: show_selected_body_parts(vars, left_frame))
    vars[value].set(0)
    
    separator = ttk.Separator(right_frame, orient='horizontal')
    separator.grid(row=row_index + (6 // max_per_row), column=0, columnspan=4, sticky="ew")
    row_index += (6 // max_per_row) + 1 


root.mainloop()
