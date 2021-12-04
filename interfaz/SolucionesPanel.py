from tkinter import *
from tkinter import ttk

from modelo.ModeloSEIL import *


class SolucionesPanel(Frame):
    def sel_euler_forward(self):
        self.model.metodo_actual = EULER_FORWARD

    def sel_euler_backwards(self):
        self.model.metodo_actual = EULER_BACKWARDS

    def sel_euler_modified(self):
        self.model.metodo_actual = EULER_MODIFIED

    def sel_rk2(self):
        self.model.metodo_actual = RUNGEKUTTA2

    def sel_rk4(self):
        self.model.metodo_actual = RUNGEKUTTA4

    def sel_solve_ivp(self):
        self.model.metodo_actual = SOLVE_IVP


    def __init__(self, model: ModeloSEIL, parent=None, **kw):
        super().__init__(parent, **kw)
        #
        self.parent = parent
        self.model = model
        self['borderwidth'] = 2
        self['relief'] = 'raised'
        self.rowconfigure(1, weight=2)
        for i in range(2, 6):
            self.rowconfigure(i, weight=1)

        #
        ttk.Label(self, text="Método de solución").grid(column=1, row=0, columnspan=2)
        label_style = ttk.Style()
        label_style.theme_use('classic')  #

        eu_ad = Button(self, text='Euler hacia adelante', bg='#f4b183', highlightbackground='#f4b183',
                       command=self.sel_euler_forward,
                       fg='#ffffff', relief='flat', font=('Calibri', 12, 'normal'), height=2, width=16)
        eu_ad.grid(row=1, column=1, columnspan=1, padx=16, pady=8)
        #
        eu_at = Button(self, text='Euler hacia atrás', bg='#f4b183', highlightbackground='#f4b183',
                       command=self.sel_euler_backwards,
                       fg='#ffffff', relief='flat', font=('Calibri', 12, 'normal'), height=2, width=16)
        eu_at.grid(row=2, column=1, columnspan=1, padx=16, pady=8)
        #
        eu_mod = Button(self, text='Euler modificado', bg='#f4b183', highlightbackground='#f4b183',
                        command=self.sel_euler_modified,
                        fg='#ffffff', relief='flat', font=('Calibri', 12, 'normal'), height=2, width=16)
        eu_mod.grid(row=3, column=1, columnspan=1, padx=16, pady=8)
        #
        RK_2 = Button(self, text='Runge-Kutta 2', bg='#f4b183', highlightbackground='#f4b183',
                        command=self.sel_rk2,
                      fg='#ffffff', relief='flat', font=('Calibri', 12, 'normal'), height=2, width=16)
        RK_2.grid(row=1, column=2, columnspan=1, padx=16, pady=8)
        #
        RK_4 = Button(self, text='Runge-Kutta 4', bg='#f4b183', highlightbackground='#f4b183',
                        command=self.sel_rk4,
                      fg='#ffffff', relief='flat', font=('Calibri', 12, 'normal'), height=2, width=16)
        RK_4.grid(row=2, column=2, columnspan=1, padx=16, pady=8)

        S_IVP = Button(self, text='Solve_ivp', bg='#f4b183', highlightbackground='#f4b183',
                      command=self.sel_solve_ivp,
                      fg='#ffffff', relief='flat', font=('Calibri', 12, 'normal'), height=2, width=16)
        S_IVP.grid(row=3, column=2, columnspan=1, padx=16, pady=8)

    def start(self):
        self.mainloop()
