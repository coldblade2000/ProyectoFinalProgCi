from tkinter import *
from tkinter import ttk

from modelo.ModeloSEIL import *

import tkinter
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure

import numpy as np


class ContenidoPrincipalPanel(Frame):
    def render(self):
        S, E, I, L, t = self.model.calcularGrafica(self.model.metodo_actual)
        ax = self.ax
        ax.cla()
        metodo = self.model.metodo_actual
        TITULO = 'Solucion del modelo SEIL '
        if metodo == EULER_FORWARD:
            ax.set_title(TITULO + "(Euler hacia adelante)")
        elif metodo == EULER_BACKWARDS:
            ax.set_title(TITULO + "(Euler hacia atraz)")
        elif metodo == EULER_MODIFIED:
            ax.set_title(TITULO + "(Euler modificado)")
        elif metodo == RUNGEKUTTA2:
            ax.set_title(TITULO + "(Runge-Kutta de 2do orden)")
        elif metodo == RUNGEKUTTA4:
            ax.set_title(TITULO + "(Runge-Kutta de 4do orden)")
        elif metodo == SOLVE_IVP:
            ax.set_title(TITULO + "(Solve_ivp)")
        if self.model.funciones_visibles['S']:
            ax.plot(t, S, 'b--', label='S')
        if self.model.funciones_visibles['E']:
            ax.plot(t, E, 'g--', label='E')
        if self.model.funciones_visibles['I']:
            ax.plot(t, I, 'r--', label='I')
        if self.model.funciones_visibles['L']:
            ax.plot(t, L, 'm--', label='L')
        ax.legend()
        ax.grid()
        ax.set_ylabel("Población")
        ax.set_xlabel("t (Tiempo en años)")
        self.grafica.draw()
        self.grafica.get_tk_widget().grid(column=1, columnspan=4, row=2)

    def __init__(self, model: ModeloSEIL, parent=None, **kw):
        super().__init__(parent, **kw)
        self.model = model
        self.parent = parent
        self['borderwidth'] = 2
        self['relief'] = 'raised'
        boton_exportar = Button(self, text='Exportar', relief='flat', width=16, bg="#D0433F", fg="#ffffff")
        boton_importar = Button(self, text='Importar', relief='flat', width=16, bg="#D0433F", fg="#ffffff")
        boton_exportar.grid(column=1, row=1, columnspan=2)
        boton_importar.grid(column=2, row=1, columnspan=2)

        self.fig = plt.Figure(figsize=(8, 4), dpi=100)
        # plt.style.use('_mpl-gallery')

        self.ax = self.fig.add_subplot(111)

        self.grafica = FigureCanvasTkAgg(self.fig, master=self)
        self.render()

        self.s_var = IntVar()
        self.e_var = IntVar()
        self.i_var = IntVar()
        self.l_var = IntVar()

        self.s_var.set(1)
        self.e_var.set(1)
        self.i_var.set(1)
        self.l_var.set(1)

        s_boton = ttk.Checkbutton(self, variable=self.s_var, text="S(t)", command=self.change_selections)
        s_boton.grid(column=1, row=3)
        e_boton = ttk.Checkbutton(self, variable=self.e_var, text="E(t)", command=self.change_selections)
        e_boton.grid(column=2, row=3)
        i_boton = ttk.Checkbutton(self, variable=self.i_var, text="I(t)", command=self.change_selections)
        i_boton.grid(column=3, row=3)
        l_boton = ttk.Checkbutton(self, variable=self.l_var, text="L(t)", command=self.change_selections)
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

    def change_selections(self):
        funciones_visibles = {
            "S": self.s_var.get() == 1,
            "E": self.e_var.get() == 1,
            "I": self.i_var.get() == 1,
            "L": self.l_var.get() == 1,
        }
        self.model.funciones_visibles = funciones_visibles
        self.parent.refresh()

    def setParent(self, parent):
        self.parent = parent

    def start(self):
        self.mainloop()
