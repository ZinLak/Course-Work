from tkinter import Tk
from gui import MainApp
from modules.game_engine import PetteiaEngine

if __name__ == "__main__":
    root = Tk()
    engine = PetteiaEngine()
    app = MainApp(root)
    root.mainloop()