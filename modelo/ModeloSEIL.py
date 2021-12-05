import struct as st
from scipy.integrate import solve_ivp
import numpy as np

EULER_FORWARD = "EF"
EULER_BACKWARDS = "EB"
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
        self.funciones_visibles = {
            "S": True,
            "E": True,
            "I": True,
            "L": True,
        }

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

    def actualizar_datos(self, S, E, I, L, t):
        self.datos = {
            "S": S,
            "E": E,
            "I": I,
            "L": L,
            "t": t
        }

    def calcularGrafica(self, metodo):
        t = np.arange(0, self.anios_maximos + self.h, self.h)
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
        elif metodo == EULER_BACKWARDS:
            S, E, I, L = self.euler_backward(S, E, I, L, t)
        elif metodo == EULER_MODIFIED:
            S, E, I, L = self.euler_modified(S, E, I, L, t)
        elif metodo == RUNGEKUTTA2:
            S, E, I, L = self.runge_kutta_2(S, E, I, L, t)
        elif metodo == RUNGEKUTTA4:
            S, E, I, L = self.runge_kutta_4(S, E, I, L, t)
        elif metodo == SOLVE_IVP:
            S, E, I, L = self.solve_ivp_method(t)

        return S, E, I, L, t

    def importarDatos(self, path: str):
        file = open(path, 'rb')
        content = file.read()
        doublecount = int(len(content) / 8)
        unpacked = st.unpack("d" * doublecount, content)
        metodo = int(unpacked[-1])
        if metodo == 0:
            self.metodo_actual = EULER_FORWARD
        elif metodo == 1:
            self.metodo_actual = EULER_BACKWARDS
        elif metodo == 2:
            self.metodo_actual = EULER_MODIFIED
        elif metodo == 3:
            self.metodo_actual = RUNGEKUTTA2
        elif metodo == 4:
            self.metodo_actual = RUNGEKUTTA4
        elif metodo == 5:
            self.metodo_actual = SOLVE_IVP
        doublecount -= 1
        # self.datos = np.array(unpacked)
        file.close()
        N = doublecount // 5
        self.anios_maximos = int(unpacked[N - 1])
        t = np.array(unpacked[0:N])
        S = np.array(unpacked[N:2 * N])
        E = np.array(unpacked[2 * N: 3 * N])
        I = np.array(unpacked[3 * N: 4 * N])
        L = np.array(unpacked[4 * N: 5 * N])

        return S, E, I, L, t

    def exportarDatos(self, file):
        datos = np.concatenate((self.datos['t'], self.datos['S'], self.datos['E'], self.datos['I'], self.datos['L']))
        metodo = None
        if self.metodo_actual == EULER_FORWARD:
            metodo = 0
        elif self.metodo_actual == EULER_BACKWARDS:
            metodo = 1
        elif self.metodo_actual == EULER_MODIFIED:
            metodo = 2
        elif self.metodo_actual == RUNGEKUTTA2:
            metodo = 3
        elif self.metodo_actual == RUNGEKUTTA4:
            metodo = 4
        elif self.metodo_actual == SOLVE_IVP:
            metodo = 5

        datos = np.append(datos, metodo)
        packed = st.pack("d" * int(len(datos)), *datos)
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

    # Algoritmos de solucion

    def euler_forward(self, S, E, I, L, t):
        for i in range(1, len(t)):
            S[i] = S[i - 1] + self.h * self.FS(S[i - 1], I[i - 1], L[i - 1])
            E[i] = E[i - 1] + self.h * self.FE(S[i - 1], E[i - 1], I[i - 1], L[i - 1])
            I[i] = I[i - 1] + self.h * self.FI(S[i - 1], E[i - 1], I[i - 1], L[i - 1])
            L[i] = L[i - 1] + self.h * self.FL(I[i - 1], L[i - 1])
        return S, E, I, L

    def euler_backward(self, S, E, I, L, t):
        Sf, Ef, If, Lf = self.euler_forward(S, E, I, L, t)
        for i in range(1, len(t)):
            S[i] = S[i - 1] + self.h * self.FS(Sf[i], If[i], Lf[i])
            E[i] = E[i - 1] + self.h * self.FE(Sf[i], Ef[i], If[i], Lf[i])
            I[i] = I[i - 1] + self.h * self.FI(Sf[i], Ef[i], If[i], Lf[i])
            L[i] = L[i - 1] + self.h * self.FL(If[i], Lf[i])
        return S, E, I, L

    def euler_modified(self, S, E, I, L, t):
        # TODO Implementar
        for i in range(1, len(t)):
            print()
        return S, E, I, L

    def runge_kutta_2(self, S, E, I, L, t):
        for i in range(1, len(t)):
            kS1 = self.FS(S[i - 1], I[i - 1], L[i - 1])
            kE1 = self.FE(S[i - 1], E[i - 1], I[i - 1], L[i - 1])
            kI1 = self.FI(S[i - 1], E[i - 1], I[i - 1], L[i - 1])
            kL1 = self.FL(I[i - 1], L[i - 1])
            kS2 = self.FS(S[i - 1] + self.h * kS1, I[i - 1] + self.h * kI1, L[i - 1] + self.h * kL1)
            kE2 = self.FE(S[i - 1] + self.h * kS1, E[i - 1] + self.h * kE1, I[i - 1] + self.h * kI1,
                          L[i - 1] + self.h * kL1)
            kI2 = self.FI(S[i - 1] + self.h * kS1, E[i - 1] + self.h * kE1, I[i - 1] + self.h * kI1,
                          L[i - 1] + self.h * kL1)
            kL2 = self.FL(I[i - 1] + self.h * kI1, L[i - 1] + self.h * kL1)
            S[i] = S[i - 1] + (self.h / 2) * (kS1 + kS2)
            E[i] = E[i - 1] + (self.h / 2) * (kE1 + kE2)
            I[i] = I[i - 1] + (self.h / 2) * (kI1 + kI2)
            L[i] = L[i - 1] + (self.h / 2) * (kL1 + kL2)
        return S, E, I, L

    def runge_kutta_4(self, S, E, I, L, t):
        for i in range(1, len(t)):
            kS1 = self.FS(S[i - 1], I[i - 1], L[i - 1])
            kE1 = self.FE(S[i - 1], E[i - 1], I[i - 1], L[i - 1])
            kI1 = self.FI(S[i - 1], E[i - 1], I[i - 1], L[i - 1])
            kL1 = self.FL(I[i - 1], L[i - 1])

            kS2 = self.FS(S[i - 1] + 0.5 * self.h * kS1,
                          I[i - 1] + 0.5 * self.h * kI1,
                          L[i - 1] + 0.5 * self.h * kL1)
            kE2 = self.FE(S[i - 1] + 0.5 * self.h * kS1,
                          E[i - 1] + 0.5 * self.h * kE1,
                          I[i - 1] + 0.5 * self.h * kI1,
                          L[i - 1] + 0.5 * self.h * kL1)
            kI2 = self.FI(S[i - 1] + 0.5 * self.h * kS1,
                          E[i - 1] + 0.5 * self.h * kE1,
                          I[i - 1] + 0.5 * self.h * kI1,
                          L[i - 1] + 0.5 * self.h * kL1)
            kL2 = self.FL(I[i - 1] + 0.5 * self.h * kI1,
                          L[i - 1] + 0.5 * self.h * kL1)

            kS3 = self.FS(S[i - 1] + 0.5 * self.h * kE2,
                          I[i - 1] + 0.5 * self.h * kI2,
                          L[i - 1] + 0.5 * self.h * kL2)
            kE3 = self.FE(S[i - 1] + 0.5 * self.h * kE2,
                          E[i - 1] + 0.5 * self.h * kE2,
                          I[i - 1] + 0.5 * self.h * kI2,
                          L[i - 1] + 0.5 * self.h * kL2)
            kI3 = self.FI(S[i - 1] + 0.5 * self.h * kE2,
                          E[i - 1] + 0.5 * self.h * kE2,
                          I[i - 1] + 0.5 * self.h * kI2,
                          L[i - 1] + 0.5 * self.h * kL2)
            kL3 = self.FL(I[i - 1] + 0.5 * self.h * kI2,
                          L[i - 1] + 0.5 * self.h * kL2)

            kS4 = self.FS(S[i - 1] + self.h * kS3,
                          I[i - 1] + self.h * kI3,
                          L[i - 1] + self.h * kL3)
            kE4 = self.FE(S[i - 1] + self.h * kS3,
                          E[i - 1] + self.h * kE3,
                          I[i - 1] + self.h * kI3,
                          L[i - 1] + self.h * kL3)
            kI4 = self.FI(S[i - 1] + self.h * kS3,
                          E[i - 1] + self.h * kE3,
                          I[i - 1] + self.h * kI3,
                          L[i - 1] + self.h * kL3)
            kL4 = self.FL(I[i - 1] + self.h * kL3,
                          L[i - 1] + self.h * kL3)

            S[i] = S[i - 1] + (self.h / 6) * (kS1 + 2 * kS2 + 2 * kS3 + kS4)
            E[i] = E[i - 1] + (self.h / 6) * (kE1 + 2 * kE2 + 2 * kE3 + kE4)
            I[i] = I[i - 1] + (self.h / 6) * (kI1 + 2 * kI2 + 2 * kI3 + kI4)
            L[i] = L[i - 1] + (self.h / 6) * (kL1 + 2 * kL2 + 2 * kL3 + kL4)
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
