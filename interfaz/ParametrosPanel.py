from tkinter import *
from tkinter import ttk


class ParametrosPanel(Frame):
    def __init__(self, parent=None, **kw):
        super().__init__(parent, **kw)
        self['borderwidth'] = 2
        self['relief'] = 'raised'
        self.rowconfigure(1, weight=2)
        for i in range(2, 6):
            self.rowconfigure(i, weight=1)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        ttk.Label(self, text='Parametros').grid(column=1, row=1, columnspan=2)
        label_style = ttk.Style()
        label_style.configure('BW.TLabel',
                              background='#f4b183',
                              foreground='white'
                              )
        beta_label = ttk.Label(self, width=20, text='β', anchor='center', style='BW.TLabel')
        lambda_label = ttk.Label(self, width=20, text='Λ', anchor='center', style='BW.TLabel')
        phi_label = ttk.Label(self, width=20, text='Φ', anchor='center', style='BW.TLabel')
        mu_label = ttk.Label(self, width=20, text='μ', anchor='center', style='BW.TLabel')

        for idx, i in enumerate([beta_label, lambda_label, phi_label, mu_label]):
            i.grid(column=1, row=2 + idx, padx=4, pady=2)

        beta_var = StringVar()
        lambda_var = StringVar()
        phi_var = StringVar()
        mu_var = StringVar()

        beta_entry = ttk.Entry(self, textvariable=beta_var)
        lambda_entry = ttk.Entry(self, textvariable=lambda_var)
        phi_entry = ttk.Entry(self, textvariable=phi_var)
        mu_entry = ttk.Entry(self, textvariable=mu_var)

        for idx, i in enumerate([beta_entry, lambda_entry, phi_entry, mu_entry]):
            i.grid(column=2, row=2 + idx, ipadx=2, ipady=1)

    def start(self):
        self.mainloop()
