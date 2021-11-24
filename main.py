from tkinter import *
from tkinter import ttk

from interfaz.ContenidoPrincipalPanel import ContenidoPrincipalPanel
from interfaz.ParametrosPanel import ParametrosPanel
from interfaz.SolucionesPanel import SolucionesPanel
from modelo.ModeloSEIL import ModeloSEIL

class MainInterface(ttk.Frame):
    def __init__(self, parent=None, **kw):
        super().__init__(parent, **kw)
        self.model = None
        self.soluciones = None
        self.parametros = None
        self.contenidoPrincipal = None

    def registerPanels(self, contenidoPrincipal, parametros, soluciones, model):
        self.model = model
        self.soluciones = soluciones
        self.parametros = parametros
        self.contenidoPrincipal = contenidoPrincipal


    def refresh(self, β_var, Λ_var, Φ_var, μ_var, δ_var, p_var, k_var,
                            r1_var, r2_var, γ_var, d1_var, d2_var):
        print("refresh", β_var, Λ_var, Φ_var, μ_var, δ_var, p_var, k_var,
                            r1_var, r2_var, γ_var, d1_var, d2_var)

root = None

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Creamos la pantalla root y el frame de contenido mainframe
    root = Tk()
    root.geometry('1200x800')
    root.title("Proyecto Final Programacion Cientifica")
    mainframe = MainInterface(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=1, columnspan=2, sticky=(N, W, E, S))
    root['borderwidth'] = 2
    root['relief'] = 'raised'

    model = ModeloSEIL()

    exit_button = Button(root, text='X', command=quit, bg='#cb4f52',
                         fg='#ffffff', relief='flat', width=16)
    exit_button.grid(column=0, row=0)

    root.columnconfigure(1, weight=1)
    root.rowconfigure(1, weight=1)

    mainframe.columnconfigure(1, weight=1)
    mainframe.columnconfigure(2, weight=1)
    mainframe.rowconfigure(1, weight=1)
    mainframe.rowconfigure(2, weight=1)

    contenido_principal_panel = ContenidoPrincipalPanel(model, mainframe)
    contenido_principal_panel.grid(column=1, row=1, rowspan=2)
    parametros_panel = ParametrosPanel(model, mainframe)
    parametros_panel.grid(column=2, row=1, ipadx=40, ipady=40)
    soluciones_panel = SolucionesPanel(model, mainframe)
    soluciones_panel.grid(column=2, row=2)

    contenido_principal_panel.start()
    parametros_panel.start()
    soluciones_panel.start()
    mainframe.registerPanels(contenido_principal_panel, parametros_panel, soluciones_panel, model)
    root.mainloop()


def quit():
    root.destroy()

