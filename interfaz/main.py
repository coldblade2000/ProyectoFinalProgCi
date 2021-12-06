from tkinter import *
from tkinter import ttk

from interfaz.ContenidoPrincipalPanel import ContenidoPrincipalPanel
from interfaz.ParametrosPanel import ParametrosPanel
from interfaz.SolucionesPanel import SolucionesPanel
from modelo.ModeloSEIL import ModeloSEIL

# Clase que gestiona la interfaz en general y contiene los otros paneles
class MainInterface(ttk.Frame):
    def __init__(self, parent=None, **kw):
        super().__init__(parent, **kw)
        self.model = None
        self.soluciones = None
        self.parametros = None
        self.contenidoPrincipal = None

    #Se registran las referencias a otros paneles con esta clase
    def registerPanels(self, contenidoPrincipal, parametros, soluciones, model):
        self.model = model
        self.soluciones = soluciones
        self.parametros = parametros
        self.contenidoPrincipal = contenidoPrincipal

    # Metodo que le indica al panel de contenido principal que deberia renderear otra vez la grafica,despues
    # de que se hizo un cambio al modelo
    def refresh(self):
        self.contenidoPrincipal.render()


root = None

if __name__ == '__main__':
    # Creamos la pantalla root y el frame de contenido mainframe
    root = Tk()
    root.geometry('1400x800')
    root.title("Proyecto Final Programacion Cientifica")
    mainframe = MainInterface(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=1, columnspan=2, sticky=(N, W, E, S))
    root['borderwidth'] = 2
    root['relief'] = 'raised'

    #inicializamos nuestra instancia del ModeloSEIL
    model = ModeloSEIL()

    # Creamos el boton para cerrar la aplicacion
    exit_button = Button(root, text='X', command=quit, bg='#cb4f52', highlightbackground='#cb4f52',
                         fg='#ffffff', relief='flat', width=16)
    exit_button.grid(column=0, row=0)

    root.columnconfigure(1, weight=1)
    root.rowconfigure(1, weight=1)

    mainframe.columnconfigure(1, weight=1)
    mainframe.columnconfigure(2, weight=1)
    mainframe.rowconfigure(1, weight=1)
    mainframe.rowconfigure(2, weight=1)

    # instanciamos y colocamos los paneles de contenido, soluciones y parametros
    contenido_principal_panel = ContenidoPrincipalPanel(model, mainframe)
    contenido_principal_panel.grid(column=1, row=1, rowspan=2)
    parametros_panel = ParametrosPanel(model, mainframe)
    parametros_panel.grid(column=2, row=1, ipadx=40, ipady=40)
    soluciones_panel = SolucionesPanel(model, mainframe)
    soluciones_panel.grid(column=2, row=2)

    # Registramos los paneles con el mainframe y les pasamos la referencia al mainframe
    mainframe.registerPanels(contenido_principal_panel, parametros_panel, soluciones_panel, model)
    contenido_principal_panel.setParent(mainframe)
    parametros_panel.setParent(mainframe)
    soluciones_panel.setParent(mainframe)
    # Corremos la interfaz
    contenido_principal_panel.start()
    parametros_panel.start()
    soluciones_panel.start()
    root.mainloop()

# Este metodo cierra la aplicacion cuando se espicha el boton de cerrar
def quit():
    root.destroy()
