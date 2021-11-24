from tkinter import *
from tkinter import ttk

from modelo.ModeloSEIL import ModeloSEIL


class ContenidoPrincipalPanel(Frame):
    def __init__(self, model: ModeloSEIL, parent=None,  **kw):
        super().__init__(parent, **kw)

        ttk.Label(self, text=__name__).pack()

    def start(self):
        self.mainloop()
