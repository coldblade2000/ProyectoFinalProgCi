import struct as st

import numpy as np

EULER_FORWARD = "EF"
EULER_BACKWARS = "EB"
RUNGEKUTTA2 = "RK2"
RUNGEKUTTA4 = "RK4"


class ModeloSEIL:
    def __init__(self):
        #   fuente: https://bloqueneon.uniandes.edu.co/content/enforced/51408-202120_IBIO2240_01/Proyecto%20final/Cap%2016.pdf pg 4
        # VARIABLES MATEMATICAS
        # β beta
        self.β = 0.025
        # Λ lambda
        self.Λ = 1 / 2
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

        # VARIABLES DEL MUNDO
        self.datos = np.empty(0)

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
        self.calcularGrafica()

    def calcularGrafica(self, metodo):
        # TODO calcular esto
        if metodo == EULER_FORWARD:
            print(EULER_FORWARD)

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
        return self.Λ + self.β * s * (i + self.δ * l) - self.μ * s

    def FE(self, s, e, i, l):
        return self.β * (1 - self.p) * s * (i + self.δ * l) + self.r2 * i - (self.μ + self.k * (1 - self.r1)) * e

    def SI(self, s, e, i, l):
        return self.β * self.p * s * (i + self.δ * l) + self.k * \
               (1 - self.r1) * e + self.γ * l - (self.μ + self.d1 + self.Φ * (1 - self.r2) + self.r2) * i

    def SL(self, i, l):
        return self.Φ * (1 - self.r2) * i - (self.μ + self.d2 + self.γ) * l
