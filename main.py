from tkinter import *
from tkinter import ttk

from interfaz.ContenidoPrincipalPanel import ContenidoPrincipalPanel
from interfaz.ParametrosPanel import ParametrosPanel
from interfaz.SolucionesPanel import SolucionesPanel

root = None

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Creamos la pantalla root y el frame de contenido mainframe
    root = Tk()
    root.geometry('1200x800')
    root.title("Proyecto Final Programacion Cientifica")
    mainframe = ttk.Frame(root, padding=" 3 3 12 12")
    mainframe.grid(column=0, row=1, columnspan=2, sticky=(N, W, E, S))
    mainframe['borderwidth'] = 2
    mainframe['relief'] = 'solid'

    exit_button = Button(root, text='X', command=quit, bg='#cb4f52',
                         fg='#ffffff', relief='flat', width=16)
    exit_button.grid(column=0, row=0)

    root.columnconfigure(1, weight=1)
    root.rowconfigure(1, weight=1)

    mainframe.columnconfigure(1, weight=1)
    mainframe.columnconfigure(2, weight=1)
    mainframe.rowconfigure(1, weight=1)
    mainframe.rowconfigure(2, weight=1)

    contenido_principal_panel = ContenidoPrincipalPanel(mainframe)
    contenido_principal_panel.grid(column=1, row=1, rowspan=2)
    parametros_panel = ParametrosPanel(mainframe)
    parametros_panel.grid(column=2, row=1)
    soluciones_panel = SolucionesPanel(mainframe)
    soluciones_panel.grid(column=2, row=2)

    contenido_principal_panel.start()
    parametros_panel.start()
    soluciones_panel.start()

    root.mainloop()


def quit():
    root.destroy()
