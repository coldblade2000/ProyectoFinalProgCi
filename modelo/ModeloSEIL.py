import struct as st

import numpy as np


class ModeloSEIL():
    def __init__(self):


        # VARIABLES MATEMATICAS
        # β beta
        self.coef_transmision = 0
        # Λ lambda
        self.tasa_reclutamiento_suceptibles = 0
        # Φ, phi
        self.tasa_infectados_resultan_perdidos = 0
        # μ, mu
        self.tasa_muertes_naturales = 0

        # CONSTANTES MATEMATICAS
        #   fuente: https://bloqueneon.uniandes.edu.co/content/enforced/51408-202120_IBIO2240_01/Proyecto%20final/Cap%2016.pdf pg 4
        δ = 1
        p = 0.3
        k = 0.005
        r1 = 0
        r2 = 0.8182
        γ = 0.01
        d1 = 0.0227
        d2 = 0.20

        self.constantes = {
            "δ": δ,
            "p": p,
            "k": k,
            "r1": r1,
            "r2": r2,
            "γ": γ,
            "d1": d1,
            "d2": d2,
        }
        # VARIABLES DEL MUNDO
        self.datos = np.empty()

    def actualizarValores(self, beta, lambda_var, phi, mu):
        self.coef_transmision = beta
        self.tasa_reclutamiento_suceptibles = lambda_var
        self.tasa_infectados_resultan_perdidos = phi
        self.tasa_muertes_naturales = mu
        self.calcularGrafica()

    def calcularGrafica(self):
        # TODO calcular esto
        print('TEMPORAL, BORRAME')

    def importarDatos(self, path: str):
        file = open(path, 'rb')
        content = file.read()
        doublecount = int(len(content) / 4)
        unpacked = st.unpack("d" * doublecount, content)
        self.datos = np.array(unpacked)
        file.close()

    def exportarDatos(self, path):
        file = open(path, 'wb')
        packed = st.pack("d"*int(len(self.datos)), *self.datos)
        file.write(packed)
        file.close()



