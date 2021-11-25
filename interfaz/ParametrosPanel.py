from tkinter import *
from tkinter import ttk

from modelo.ModeloSEIL import ModeloSEIL


class ParametrosPanel(Frame):
    def __init__(self, model: ModeloSEIL, parent=None, **kw):
        super().__init__(parent, **kw)
        self.parent = parent
        self['borderwidth'] = 2
        self['relief'] = 'raised'
        self.rowconfigure(1, weight=2)
        for i in range(2, 8):
            self.rowconfigure(i, weight=1)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)

        ttk.Label(self, text='Parametros').grid(column=1, row=1, columnspan=4)
        label_style = ttk.Style()
        label_style.theme_use('classic')
        label_style.configure('BW.TLabel',
                              background='#f4b183',
                              highlightbackground='#f4b183',
                              foreground='white'
                              )
        β_label = ttk.Label(self, width=12, text='β', anchor='center', style='BW.TLabel')
        Λ_label = ttk.Label(self, width=12, text='Λ', anchor='center', style='BW.TLabel')
        Φ_label = ttk.Label(self, width=12, text='Φ', anchor='center', style='BW.TLabel')
        μ_label = ttk.Label(self, width=12, text='μ', anchor='center', style='BW.TLabel')
        δ_label = ttk.Label(self, width=12, text='δ', anchor='center', style='BW.TLabel')
        p_label = ttk.Label(self, width=12, text='p', anchor='center', style='BW.TLabel')

        k_label = ttk.Label(self, width=12, text='k', anchor='center', style='BW.TLabel')
        r1_label = ttk.Label(self, width=12, text='r1', anchor='center', style='BW.TLabel')
        r2_label = ttk.Label(self, width=12, text='r2', anchor='center', style='BW.TLabel')
        γ_label = ttk.Label(self, width=12, text='γ', anchor='center', style='BW.TLabel')
        d1_label = ttk.Label(self, width=12, text='d1', anchor='center', style='BW.TLabel')
        d2_label = ttk.Label(self, width=12, text='d2', anchor='center', style='BW.TLabel')

        for idx, i in enumerate(
                [β_label, Λ_label, Φ_label, μ_label, δ_label, p_label, k_label, r1_label, r2_label, γ_label, d1_label,
                 d2_label]):
            i.grid(column=1 + (idx // 6 * 2), row=2 + idx % 6, padx=2, pady=2)

        self.β_var = DoubleVar()
        self.β_var.set(model.β)
        self.Λ_var = DoubleVar()
        self.Λ_var.set(model.Λ)
        self.Φ_var = DoubleVar()
        self.Φ_var.set(model.Φ)
        self.μ_var = DoubleVar()
        self.μ_var.set(model.μ)
        self.δ_var = DoubleVar()
        self.δ_var.set(model.δ)
        self.p_var = DoubleVar()
        self.p_var.set(model.p)
        self.k_var = DoubleVar()
        self.k_var.set(model.k)
        self.r1_var = DoubleVar()
        self.r1_var.set(model.r1)
        self.r2_var = DoubleVar()
        self.r2_var.set(model.r2)
        self.γ_var = DoubleVar()
        self.γ_var.set(model.γ)
        self.d1_var = DoubleVar()
        self.d1_var.set(model.d1)
        self.d2_var = DoubleVar()
        self.d2_var.set(model.d2)

        β_entry = Entry(self, textvariable=self.β_var)
        Λ_entry = Entry(self, textvariable=self.Λ_var)
        Φ_entry = Entry(self, textvariable=self.Φ_var)
        μ_entry = Entry(self, textvariable=self.μ_var)
        δ_entry = Entry(self, textvariable=self.δ_var)
        p_entry = Entry(self, textvariable=self.p_var)
        k_entry = Entry(self, textvariable=self.k_var)
        r1_entry = Entry(self, textvariable=self.r1_var)
        r2_entry = Entry(self, textvariable=self.r2_var)
        γ_entry = Entry(self, textvariable=self.γ_var)
        d1_entry = Entry(self, textvariable=self.d1_var)
        d2_entry = Entry(self, textvariable=self.d2_var)

        for idx, i in enumerate(
                [β_entry, Λ_entry, Φ_entry, μ_entry, δ_entry, p_entry, k_entry, r1_entry, r2_entry, γ_entry, d1_entry,
                 d2_entry]):
            i.grid(column=2 + (idx // 6 * 2), row=2 + idx % 6, ipadx=2, ipady=1)

        refresh_btn = Button(self, text='Refresh', command=self.refresh, bg='#f4b183', highlightbackground='#f4b183',
                             fg='#ffffff', relief='flat', width=16)
        refresh_btn.grid(row=8, column=1, columnspan=4, padx=20, pady=20)
    def refresh(self):

        self.parent.refresh(self.β_var, self.Λ_var, self.Φ_var, self.μ_var, self.δ_var, self.p_var, self.k_var,
                            self.r1_var, self.r2_var, self.γ_var, self.d1_var, self.d2_var)

    def start(self):
        self.mainloop()
