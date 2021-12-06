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

# El panel donde esta la grafica, los años de simulacion, import, export  y los toggles para seleccionar que
# ecuaciones se quieren ver en la grafica
class ContenidoPrincipalPanel(Frame):
    # Metodo que renderea la grafica segun los datos obtenidos del modelo.Estos pueden ser datos calculados o importados
    def render(self, path=None):
        S, E, I, L, t = None, None, None, None, None
        TITULO = 'Solucion del modelo SEIL '
        # Se consiguen los datos del modelo.Se calculan o si se le pasa un path a render(),importa los datos de ese file
        if path == None:
            S, E, I, L, t = self.model.calcularGrafica(self.model.metodo_actual)
        else:
            TITULO = TITULO + 'importado '
            S, E, I, L, t = self.model.importarDatos(path)
        # Guarda los datos obtenidos en el modelo
        self.model.actualizar_datos(S, E, I, L, t)
        # Consigue referencias al axe y el metodo de solucion
        ax = self.ax
        ax.cla()
        metodo = self.model.metodo_actual

        # Cambia el titulo segun el metodo de solucion seleccionado en la grafica
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

        # Grafica las ecuaciones en la grafica dependiendo si estan seleccionadas o no
        if self.model.funciones_visibles['S']:
            ax.plot(t, S, 'b--', label='S')
        if self.model.funciones_visibles['E']:
            ax.plot(t, E, 'g--', label='E')
        if self.model.funciones_visibles['I']:
            ax.plot(t, I, 'r--', label='I')
        if self.model.funciones_visibles['L']:
            ax.plot(t, L, 'm--', label='L')

        # Muestra la leyenda y el grid en la grafica, pone las etiquetas de los ejes y muestra la grafica
        ax.legend()
        ax.grid()
        ax.set_ylabel("Población")
        ax.set_xlabel("t (Tiempo en años)")
        self.grafica.draw()
        self.grafica.get_tk_widget().grid(column=1, columnspan=4, row=2)

    # Empieza el proceso de importar archivo de simulacion
    def import_file(self):
        # Solo acepta archivos de tipo .sim
        filetypes = (('simulation files', '*.sim'),)

        # Abre una ventana que le permite a uno seleccionar un archivo para abrir y guarda su ruta
        filename = fd.askopenfilename(
            title='Open a simulation file',
            initialdir='/',
            filetypes=filetypes)

        # Le pasa la ruta a self.render()
        self.render(path=filename)

    # Empieza el proceso de exportar la simulacion actual. Le pide al usuario donde quiere guardar el archivo
    def export_file(self):
        files = [('Simulation files', '*.sim')]
        file = asksaveasfile(mode='wb', filetypes=files, defaultextension=files)
        # Le pasa el archivo al modelo para que exporte los datos ahi
        self.model.exportarDatos(file)

    # Se inicializa el panel
    def __init__(self, model: ModeloSEIL, parent=None, **kw):
        super().__init__(parent, **kw)
        self.model = model
        self.parent = parent
        self['borderwidth'] = 2
        self['relief'] = 'raised'

        # Crea los botones para exportar e importar datos
        boton_exportar = Button(self, text='Exportar', relief='flat', width=16, bg="#D0433F", fg="#ffffff",
                                command=self.export_file)
        boton_importar = Button(self, text='Importar', relief='flat', width=16, bg="#D0433F", fg="#ffffff",
                                command=self.import_file)
        boton_exportar.grid(column=1, row=1, columnspan=2)
        boton_importar.grid(column=2, row=1, columnspan=2)

        # Inicializa la figura y el axe de la grafica
        self.fig = plt.Figure(figsize=(8, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.grafica = FigureCanvasTkAgg(self.fig, master=self)
        # Renderea la grafica
        self.render()

        # Inicializa los IntVars que representa si los checkboxes de las funciones estan seleccionados
        self.s_var = IntVar()
        self.e_var = IntVar()
        self.i_var = IntVar()
        self.l_var = IntVar()
        self.s_var.set(1)
        self.e_var.set(1)
        self.i_var.set(1)
        self.l_var.set(1)

        # Crea los checkbuttons para cada funcion
        s_boton = ttk.Checkbutton(self, variable=self.s_var, text="S(t)", command=self.change_selections)
        s_boton.grid(column=1, row=3)
        e_boton = ttk.Checkbutton(self, variable=self.e_var, text="E(t)", command=self.change_selections)
        e_boton.grid(column=2, row=3)
        i_boton = ttk.Checkbutton(self, variable=self.i_var, text="I(t)", command=self.change_selections)
        i_boton.grid(column=3, row=3)
        l_boton = ttk.Checkbutton(self, variable=self.l_var, text="L(t)", command=self.change_selections)
        l_boton.grid(column=4, row=3)

        # Se crea la caja de texto para los años que deberia correr la simulacion
        tiempo = ttk.Label(master=self, text="Tiempo de simulación")
        tiempo.grid(column=2, row=4)
        self.tiempo_var = IntVar()
        self.tiempo_var.set(self.model.anios_maximos)
        tiempo_caja = ttk.Entry(self, textvariable=self.tiempo_var)
        tiempo_caja.grid(column=2, row=5)

        date = ttk.Label(master=self, text="Años")
        date.grid(column=3, row=5)

        # Cre un boton para refrescar la grafica segun los cambios de los años de simulacion
        refresh_btn = Button(self, text='Refrescar', bg='#f4b183', highlightbackground='#f4b183',
                             command=self.cambiar_anios,
                             fg='#ffffff', relief='flat', font=('Calibri', 12, 'normal'), height=2, width=16)
        refresh_btn.grid(row=5, column=4, padx=16, pady=8)

    # Guarda los años de simulacion en el modelo
    def cambiar_anios(self):
        self.model.anios_maximos = self.tiempo_var.get()
        self.render()

    # Le informa al modelo que funciones se quieren mostrar y refresca la grafica
    def change_selections(self):
        funciones_visibles = {
            "S": self.s_var.get() == 1,
            "E": self.e_var.get() == 1,
            "I": self.i_var.get() == 1,
            "L": self.l_var.get() == 1,
        }
        self.model.funciones_visibles = funciones_visibles
        self.parent.refresh()

    # Guarda referencia al mainframe
    def setParent(self, parent):
        self.parent = parent

    # Ejecuta el panel
    def start(self):
        self.mainloop()
