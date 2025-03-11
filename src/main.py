import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from window_config import prepare_window

root = tk.Tk()
prepare_window(root)

def show_message():
    showinfo("Message", "Hello, World!")


# Create a main frame to hold the two sections
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Left section with a button
left_frame = tk.Frame(main_frame, width=600, bg="lightgray")
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

button = ttk.Button(left_frame, text="Click Me", command=show_message)
button.pack(pady=20, padx=20)

# Right section with checkboxes
right_frame = tk.Frame(main_frame, width=200, bg="white")
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

ttk.Label(right_frame, text="Options").grid(row=0, column=0, columnspan=4, pady=10)

row_index = 1
max_per_row = 3
vars = {}
for value in ["Head", "Wings", "Legs"]:
    ttk.Label(right_frame, text=value).grid(row=row_index, column=0, padx=10, pady=5, sticky="w")
    vars.append(tk.IntVar())

    # TODO: Hacer que wrapee como Dios manda solo si se llega a chocar con la pantalla
    for i in range(6):  
        col_index = (i % max_per_row) + 1  
        row_offset = i // max_per_row  
        radiobutton = ttk.Radiobutton(right_frame, text="Option " + str(i), variable=vars[value], value=i)
        radiobutton.grid(row=row_index + row_offset, column=col_index, padx=5, pady=5)
    vars[value].set(-1)

    row_index += (6 // max_per_row) + 1 


root.mainloop()
