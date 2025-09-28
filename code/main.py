# Hinweis: Programm immer aus dem Projekt-Root starten,
# sonst funktionieren die relativen Pfade zu "audio/" und "images/" nicht.
# Das heißt:  
# cd SCS-JumpKing
# python code/main.py

from menu import *

if __name__ == "__main__":
    Menu().run()