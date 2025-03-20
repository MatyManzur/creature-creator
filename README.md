# Home Assignment 1
**Subject**: Application or use cases of various design patterns
**Students**:
- Mauro Leandro Baez
- Matias Manzur
  
**Lecturer**: Maxim Glaida
**Date**: 20/03/2025

## What is this?
We decided to make a sims-like character creator, but instead of creating humans, you create animal mixes! It's as weird as it sounds... The animals themselves are made in 32 bits artstyle, so it might be a good idea to not maximize the window.

## How to run

**Requirements**: 
- `python3.10` or higher
- `pip`

In order to run our project, just execute `install.sh` (or `install.bat` in Windows) in order to create a virtual environment and install the dependencies (Pillow & tk).

Afterwards you can just run `./run.sh` (or `run.bat` in Windows).

**Note:** If by any reason pip is unable to install tkinter, and your system's python installation does not include it by default, you may need to install it with something like `sudo apt install python3-tk`. It is a package used for generating the GUI.

## Design Patterns Applied
The 3 design patterns chosen are: **Memento**, **Command** & **Singleton**.

You can find Memento pattern in the `creator.py` file. It is used for the undo and redo buttons, by generating a `Snapshot` of the app main state.

Undo and Redo are just two examples of the Commands we have implemented. You can find all of them in the `command.py` file. The commands themselves are built in the `main.py` file using the Builder pattern. Each command contains an execute() method, that is in charge of making the corresponding changes.

Finally, the Singleton pattern is used in the `creator.py` and `command.py` files. Singleton is used in the `VersionManager`, in the `Creator` and in the `CommandBuilder`! 

