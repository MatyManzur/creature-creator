import tkinter as tk
from body_part import BodyPartType
from command import GenerateStoryCommand, RedoCommand, UndoCommand, generate_random_command, generate_simple_command
from creator import Creator
from tkinter import ttk


def prepare_window(window: tk):
    # Create the window
    window.title("Build your Pet")
    #window.geometry("400x400")
    window.configure(background="black")

class CreatureScreen():

    def __init__(self, frame):
        self.frame = frame
        self.creator = Creator.get_instance()

    def update_screen(self):
        #print(f"{self.creator.get_selected_body_part(BodyPartType.HEAD)}, {self.creator.get_selected_body_part(BodyPartType.TORSO)}, {self.creator.get_selected_body_part(BodyPartType.LEGS)}, {self.creator.get_selected_body_part(BodyPartType.WINGS)}")
        head_sprite = self.creator.get_selected_body_part(BodyPartType.HEAD).get_sprite()
        torso_sprite = self.creator.get_selected_body_part(BodyPartType.TORSO).get_sprite()
        legs_sprite = self.creator.get_selected_body_part(BodyPartType.LEGS).get_sprite()
        wings_sprite = self.creator.get_selected_body_part(BodyPartType.WINGS).get_sprite()

        for widget in self.frame.winfo_children():
            widget.destroy()

        canvas = tk.Canvas(self.frame, bg="lightgray")
        canvas.pack(fill=tk.BOTH, expand=True)

        y_offset = 50
        canvas.create_image(100 - wings_sprite.width()/2, 1.35*y_offset, anchor=tk.NW, image=wings_sprite)
        for sprite in [head_sprite, torso_sprite, legs_sprite]:
            img = sprite
            canvas.create_image(100 - img.width()/2, y_offset, anchor=tk.NW, image=img)
            y_offset += img.height()
            canvas.image = img  # Keep a reference to avoid garbage collection


def prepare_options_panel(root, right_frame, creator):
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


def prepare_footer(footer):
    footer_label = ttk.Label(footer, text="Ctrl+Z: Undo | Ctrl+Y: Redo | Ctrl+R: Randomize")
    footer_label.pack(side=tk.LEFT, padx=10)

def prepare_story_panels(root, creator: Creator, MODELS):
    story_panel = tk.Frame(root, width=400, height=100, bg="lightblue")
    story_panel.grid(row=2, column=0, sticky="ew")
    story_panel.grid_propagate(False)  # Prevents auto-resizing

    story_choices_panel = tk.Frame(root, width=400, height=100, bg="lightblue")
    story_choices_panel.grid(row=3, column=0, sticky="ew")
    story_choices_panel.grid_propagate(False)  # Prevents auto-resizing

    def update_story():
        story = creator.get_story()
        story_text.config(state="normal")
        story_text.delete(1.0, tk.END)
        story_text.insert(tk.END, story)
        story_text.config(state="disabled")

    model_var = tk.StringVar(value=MODELS[0])
    # Create a frame to center the radio buttons
    model_frame = tk.Frame(story_choices_panel)
    model_frame.grid(row=0, column=0, pady=5)

    # Create radio buttons for each model
    ttk.Label(model_frame, text='Model options: ').grid(row=0, column=0, padx=10, pady=5, sticky="w")
    for index, model in enumerate(MODELS):
        model_radio = ttk.Radiobutton(model_frame, text=model, variable=model_var, value=model)
        model_radio.grid(row=0, column=index+1, padx=5, pady=5, sticky="w")

    # Center the Generate Story button
    generate_story_button = ttk.Button(
        story_choices_panel, 
        text="Generate Story", 
        command=lambda: GenerateStoryCommand(model_var.get()).execute()
    )
    generate_story_button.grid(row=1, column=0, padx=5, pady=10)
    story_choices_panel.grid_columnconfigure(0, weight=1)  # Center the button horizontally

    story_scrollbar = tk.Scrollbar(story_panel, orient=tk.VERTICAL)
    story_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    story_text = tk.Text(story_panel, wrap="word", height=10, state="disabled", bg="white", fg="black", yscrollcommand=story_scrollbar.set)
    story_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    story_scrollbar.config(command=story_text.yview)

    def show_temporary_cache_message():
        message_label = tk.Label(model_frame, text="(Story was cached!)", bg="yellow", fg="black")
        message_label.grid(row=0, column=3, padx=5, pady=10)
        model_frame.after(2000, message_label.destroy)

    creator.set_cached_callback(show_temporary_cache_message)
    creator.subscribe_callback(update_story)




