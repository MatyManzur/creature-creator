
from tkinter import Tk
from tkinter.messagebox import showinfo


def prepare_window(window: Tk):
    # Create the window
    window.title("Build your Pet")
    #window.geometry("400x400")
    window.configure(background="black")

def go_back():
    showinfo("Message", "Going back!")


def show_message():
    showinfo("Message", "Hello, World!")

def ChangeMe(value, option):
    print("Changing value of " + value + " to " + str(option))
