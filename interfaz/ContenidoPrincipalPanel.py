from tkinter import *
from tkinter import ttk

from modelo.ModeloSEIL import ModeloSEIL

import tkinter
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure

import numpy as np


class ContenidoPrincipalPanel(Frame):
    def __init__(self, model: ModeloSEIL, parent=None, **kw):
        super().__init__(parent, **kw)
        self['borderwidth'] = 2
        self['relief'] = 'raised'
        boton_exportar = Button(self, text='Exportar', relief='flat', width=16, bg="#D0433F")
        boton_importar = Button(self, text='Importar', relief='flat', width=16, bg="#D0433F")
        boton_exportar.grid(column=1, row=1, columnspan=2)
        boton_importar.grid(column=2, row=1, columnspan=2)

        fig = plt.Figure(figsize=(8, 4), dpi=100)
        t = np.arange(0, 3, .01)
        # plt.style.use('_mpl-gallery')

        ax = fig.add_subplot(111)
        ax.plot(linewidth=2.0)  # aqui va la ecuacion ax.plot(t, t**2, line...)
        ax.set_ylabel("Población")
        ax.set_xlabel("t (Tiempo en años)")

        grafica = FigureCanvasTkAgg(fig, master=self)
        grafica.draw()
        grafica.get_tk_widget().grid(column=1, columnspan=4, row=2)

        s_var = BooleanVar()
        e_var = BooleanVar()
        i_var = BooleanVar()
        l_var = BooleanVar()

        s_boton = ttk.Checkbutton(self, variable=s_var, text="S(t)")
        s_boton.grid(column=1, row=3)
        e_boton = ttk.Checkbutton(self, variable=e_var, text="E(t)")
        e_boton.grid(column=2, row=3)
        i_boton = ttk.Checkbutton(self, variable=i_var, text="I(t)")
        i_boton.grid(column=3, row=3)
        l_boton = ttk.Checkbutton(self, variable=l_var, text="L(t)")
        l_boton.grid(column=4, row=3)

        tiempo = ttk.Label(master=self, text="Tiempo de simulación")
        tiempo.grid(column=2, row=4)

        a_var = IntVar()
        b_var = IntVar()
        c_var = IntVar()

        a_caja = ttk.Entry(self, textvariable=a_var)
        a_caja.grid(column=1, row=5)
        b_caja = ttk.Entry(self, textvariable=b_var)
        b_caja.grid(column=2, row=5)
        c_caja = ttk.Entry(self, textvariable=c_var)
        c_caja.grid(column=3, row=5)

        date = ttk.Label(master=self, text="Años")
        date.grid(column=4, row=5)

    def start(self):
        self.mainloop()
