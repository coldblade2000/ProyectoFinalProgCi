from modelo.ModeloSEIL import *
import matplotlib.pyplot as plt
import numpy as np

modelo = ModeloSEIL()

S, E, I, L, t = modelo.calcularGrafica(EULER_BACKWARDS)

plt.plot(t, S, 'b--', label='S')
plt.plot(t, E, 'g--', label='E')
plt.plot(t, I, 'r--', label='I')
plt.plot(t, L, 'm--', label='L')
S, E, I, L, t = modelo.calcularGrafica(SOLVE_IVP)
plt.plot(t, S, 'b-', label='Sip')
plt.plot(t, E, 'g-', label='Eip')
plt.plot(t, I, 'r-', label='Iip')
plt.plot(t, L, 'm-', label='Lip')
plt.legend()
plt.grid()
plt.show()