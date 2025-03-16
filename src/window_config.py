
from tkinter import Tk
from tkinter.messagebox import showinfo


def prepare_window(window: Tk):
    # Create the window
    window.title("Build your Pet")
    #window.geometry("400x400")
    window.configure(background="black")

def show_message(title: str, message: str):
    showinfo(title, message)

