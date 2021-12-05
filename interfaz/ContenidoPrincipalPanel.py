from tkinter import *
from tkinter import ttk
from tkinter.filedialog import asksaveasfile
from tkinter.messagebox import showinfo

from modelo.ModeloSEIL import *

import tkinter
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure
from tkinter import filedialog as fd
import numpy as np


class ContenidoPrincipalPanel(Frame):
    def render(self, path=None):
        S, E, I, L, t = None, None, None, None, None
        TITULO = 'Solucion del modelo SEIL '
        if path == None:
            S, E, I, L, t = self.model.calcularGrafica(self.model.metodo_actual)
        else:
            TITULO = TITULO + 'importado '
            S, E, I, L, t = self.model.importarDatos(path)
        self.model.actualizar_datos(S, E, I, L, t)
        ax = self.ax
        ax.cla()
        metodo = self.model.metodo_actual

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

    def import_file(self):
        filetypes = (
            ('simulation files', '*.sim'),
        )

        filename = fd.askopenfilename(
            title='Open a simulation file',
            initialdir='/',
            filetypes=filetypes)


        self.render(path=filename)

    def export_file(self):
        files = [('Simulation files', '*.sim')]
        file = asksaveasfile(mode='wb', filetypes=files, defaultextension=files)
        self.model.exportarDatos(file)

    def __init__(self, model: ModeloSEIL, parent=None, **kw):
        super().__init__(parent, **kw)
        self.model = model
        self.parent = parent
        self['borderwidth'] = 2
        self['relief'] = 'raised'
        boton_exportar = Button(self, text='Exportar', relief='flat', width=16, bg="#D0433F", fg="#ffffff",
                                command=self.export_file)
        boton_importar = Button(self, text='Importar', relief='flat', width=16, bg="#D0433F", fg="#ffffff",
                                command=self.import_file)
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
