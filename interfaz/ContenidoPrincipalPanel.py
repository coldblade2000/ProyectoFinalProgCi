from tkinter import *
from tkinter import ttk


class ContenidoPrincipalPanel(Frame):
    def __init__(self, parent=None, **kw):
        super().__init__(parent, **kw)

        ttk.Label(self, text=__name__).pack()

    def start(self):
        self.mainloop()
