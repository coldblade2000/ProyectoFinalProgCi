import struct as st
from scipy.integrate import solve_ivp
import numpy as np

EULER_FORWARD = "EF"
EULER_BACKWARS = "EB"
EULER_MODIFIED = "EM"
RUNGEKUTTA2 = "RK2"
RUNGEKUTTA4 = "RK4"
SOLVE_IVP = 'SI'


class ModeloSEIL:
    def __init__(self):
        #   fuente: https://bloqueneon.uniandes.edu.co/content/enforced/51408-202120_IBIO2240_01/Proyecto%20final/Cap%2016.pdf pg 4
        # VARIABLES MATEMATICAS
        # β beta
        self.β = 0.025
        # Λ lambda
        self.Λ = 2
        # Φ, phi
        self.Φ = 0.02
        # μ, mu
        self.μ = 0.0101

        self.δ = 1
        self.p = 0.3
        self.k = 0.005
        self.r1 = 0
        self.r2 = 0.8182
        self.γ = 0.01
        self.d1 = 0.0227
        self.d2 = 0.20

        # constantes
        # Valores iniciales
        self.s_0 = self.Λ / self.μ
        self.e_0 = 1
        self.i_0 = 0
        self.l_0 = 0
        self.h = 0.5

        # VARIABLES DEL MUNDO
        self.datos = np.empty(0)
        self.anios_maximos = 20
        self.metodo_actual = EULER_FORWARD

    def actualizarValores(self, β, Λ, Φ, μ, δ, p, k, r1, r2, γ, d1, d2):
        self.β = β
        self.Λ = Λ
        self.Φ = Φ
        self.μ = μ
        self.δ = δ
        self.p = p
        self.k = k
        self.r1 = r1
        self.r2 = r2
        self.γ = γ
        self.d1 = d1
        self.d2 = d2
        self.calcularGrafica(self.metodo_actual)

    def calcularGrafica(self, metodo=EULER_FORWARD):
        t = np.arange(0, self.anios_maximos, self.h)
        N = len(t)
        S = np.empty(N)
        E = np.empty(N)
        I = np.empty(N)
        L = np.empty(N)
        S[0] = self.s_0
        E[0] = self.e_0
        I[0] = self.i_0
        L[0] = self.l_0

        if metodo == EULER_FORWARD:
            S, E, I, L = self.euler_forward(S, E, I, L, t)
        elif metodo == SOLVE_IVP:
            S, E, I, L = self.solve_ivp_method(t)


        return S, E, I, L, t

    def importarDatos(self, path: str):
        file = open(path, 'rb')
        content = file.read()
        doublecount = int(len(content) / 4)
        unpacked = st.unpack("d" * doublecount, content)
        self.datos = np.array(unpacked)
        file.close()

    def exportarDatos(self, path):
        file = open(path, 'wb')
        packed = st.pack("d" * int(len(self.datos)), *self.datos)
        file.write(packed)
        file.close()

    # ecuaciones diferenciales

    def FS(self, s, i, l):
        return self.Λ - self.β * s * (i + self.δ * l) - self.μ * s

    def FE(self, s, e, i, l):
        return self.β * (1 - self.p) * s * (i + self.δ * l) + self.r2 * i - (self.μ + self.k * (1 - self.r1)) * e

    def FI(self, s, e, i, l):
        return self.β * self.p * s * (i + self.δ * l) + self.k * (1 - self.r1) * e + \
               self.γ * l - (self.μ + self.d1 + self.Φ * (1 - self.r2) + self.r2) * i

    def FL(self, i, l):
        return self.Φ * (1 - self.r2) * i - (self.μ + self.d2 + self.γ) * l

    def euler_forward(self, S, E, I, L, t):
        arr = np.array([S, E, I, L])
        for i in range(1, len(t)):
            print(i)
            S[i] = S[i - 1] + self.h * self.FS(S[i - 1], I[i - 1], L[i - 1])
            E[i] = E[i - 1] + self.h * self.FE(S[i - 1], E[i - 1], I[i - 1], L[i - 1])
            I[i] = I[i - 1] + self.h * self.FI(S[i - 1], E[i - 1], I[i - 1], L[i - 1])
            L[i] = L[i - 1] + self.h * self.FL(I[i - 1], L[i - 1])
            arr = np.array([S, E, I, L])
        return S, E, I, L

    def solve_ivp_method(self, t):
        p = (self.β, self.Λ, self.Φ, self.μ, self.δ, self.p, self.k, self.r1, self.r2, self.γ, self.d1, self.d2)
        y0 = [self.s_0, self.e_0, self.i_0, self.l_0]
        result = solve_ivp(self.s_ivp_function, (0, self.anios_maximos), y0, method='RK45', t_eval=t, args=p)
        S = result.y[0]
        E = result.y[1]
        I = result.y[2]
        L = result.y[3]
        return S, E, I, L

    def s_ivp_function(self, t, y, β, Λ, Φ, μ, δ, p, k, r1, r2, γ, d1, d2):
        s, e, i, l = y
        return np.array([Λ - β * s * (i + δ * l) - μ * s,
                        β * (1 - p) * s * (i + δ * l) + r2 * i - (μ + k * (1 - r1)) * e,
                        β * p * s * (i + δ * l) + k * (1 - r1) * e + \
                        γ * l - (μ + d1 + Φ * (1 - r2) + r2) * i,
                        Φ * (1 - r2) * i - (μ + d2 + γ) * l])
