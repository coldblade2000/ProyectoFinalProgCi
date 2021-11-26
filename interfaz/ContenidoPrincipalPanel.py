from tkinter import *
from tkinter import ttk

from modelo.ModeloSEIL import ModeloSEIL


class ContenidoPrincipalPanel(Frame):
    def __init__(self, model: ModeloSEIL, parent=None,  **kw):
        super().__init__(parent, **kw)
        
        s_var = BooleanVar()
        e_var = BooleanVar()
        i_var = BooleanVar()
        l_var = BooleanVar()
        

        s_boton = ttk.Checkbutton(self, variable = s_var, text = "S(t)")
        s_boton.grid(column = 1, row = 1)
        e_boton = ttk.Checkbutton(self, variable = e_var, text = "E(t)")
        e_boton.grid(column = 2, row = 1)
        i_boton = ttk.Checkbutton(self, variable = i_var, text = "I(t)")
        i_boton.grid(column = 3, row = 1)
        l_boton = ttk.Checkbutton(self, variable = l_var, text = "L(t)")
        l_boton.grid(column = 4, row = 1)
       
        tiempo = ttk.Label(master = self, text = "Tiempo de simulación")
        tiempo.grid(column = 2, row = 2)
        
        a_var = IntVar()
        b_var = IntVar()
        c_var = IntVar()
        
        
        a_caja = ttk.Entry(self, variable = a_var)
        a_caja.grid(column = 1, row = 3)
        b_caja = ttk.Entry(self, variable = b_var)
        b_caja.grid(column = 2, row = 3)
        c_caja = ttk.Entry(self, variable = c_var)
        c_caja.grid(column = 3, row = 3)
        
        date = ttk.Label(master = self, text = "Años")
        date.grid (column = 4, row = 3)
    def start(self):
        self.mainloop()
