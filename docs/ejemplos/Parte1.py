##
import tkinter as tk

# 1er Parte Fundamental: Definir la VEntana!  Tk()
window = tk.Tk()
window.geometry('500x400')

# 3ra Parte: Los Widgets  (Clases-Funciones)

'''Variable = Widget(master, option)'''

label = tk.Label(master=window, text='Proyecto Final', background='#853D2E').pack()


label2 = tk.Label(window,
                  text='Programación',
                  foreground='teal',
                  height=20,
                  width=30,
                  bg='yellowgreen')

label2.pack()


# 2da Parte Fundamental: "El bucle infinito"
window.mainloop()

##
import tkinter as tk
'''Entry: Ingresar una sola línea de texto'''

window = tk.Tk()
window.geometry('400x300')

Nombre = tk.Label(window, text='Escriba su nombre', fg='Teal')
Nombre.pack(side=tk.LEFT)

Nombre_In = tk.Entry(window, fg='salmon', bg='gold').pack(side=tk.RIGHT,
                                                           fill=tk.BOTH,
                                                           expand=True)

window.mainloop()

##
import tkinter as tk

window = tk.Tk()

Nombre = tk.Label(window, text='Escriba su nombre', fg='Teal').pack()

Variable = tk.StringVar()
Nombre_In = tk.Entry(window, state=tk.DISABLED, textvariable=Variable, fg='#4DDE51', bg='gold')
Nombre_In.pack()

Nombre_In.config(state=tk.NORMAL)

#print(Nombre_In.get())

n1 = Nombre_In.insert(8,'hola')

window.mainloop()

##
'''grid()'''
import tkinter as tk
'''import matplotlib
matplotlib.use("TkAgg")
import matplotlib
matplotlib.use('MacOSX')'''

window = tk.Tk()

tk.Label(window, text='Escriba su nombre', fg='Teal').grid(row=0)
tk.Label(window, text='Escriba su Apellido', fg='Teal').grid(row=1)

tk.Entry().grid(row=0, column=1)
tk.Entry(width=10).grid(row=1, column=1)

window.mainloop()

##
'''Place() y botones'''
import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")

window = tk.Tk()
window.geometry('400x300')

label = tk.Label(window, text='Valor', bg='coral').place(x=100,y=150)
Boton1 = tk.Button(window, text='Play', width=5, height=8,
                   command=window.destroy).place(x=150, y=150)

# 2da Parte Fundamental: "El bucle infinito"
window.mainloop()


##
'''Frame'''
import tkinter as tk

window2 = tk.Tk()
frame = tk.Frame(window2).pack()

Boton = tk.Button(master=frame, text='Play').pack()
Boton2 = tk.Button(master=frame, text='Jugar').pack()

window2.mainloop()


##
import tkinter as tk

border = {
    'flat': (tk.FLAT, 'coral'),
    'sunken': (tk.SUNKEN, 'yellowgreen'),
    'raised': (tk.RAISED, 'salmon'),
    'groove': (tk.GROOVE, 'gold'),
    'ridge': (tk.RIDGE, 'teal')
}

#border.get('flat')

window3 = tk.Tk()
window3.title('Programación Científica')
window3.geometry('400x300')

for nombre, funcion in border.items():
    frame = tk.Frame(master=window3, relief=funcion[0], bg='cyan',borderwidth=5)
    frame.pack(side=tk.BOTTOM)

    label = tk.Label(master=frame, text=nombre, bg=funcion[1]).pack(padx=20, pady=10, expand=True)

window3.mainloop()