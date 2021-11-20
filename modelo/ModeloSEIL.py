

class ModeloSEIL():
    def __init__(self):
        # β beta
        self.coef_transmision = 0
        # Λ lambda
        self.tasa_reclutamiento_suceptibles = 0
        # Φ, phi
        self.tasa_infectados_resultan_perdidos = 0
        # μ, mu
        self.tasa_muertes_naturales = 0

    def actualizarValores(self, beta, lambda_var, phi, mu):
        self.coef_transmision = beta
        self.tasa_reclutamiento_suceptibles = lambda_var
        self.tasa_infectados_resultan_perdidos = phi
        self.tasa_muertes_naturales = mu
        self.calcularGrafica()

    def calcularGrafica(self):
        # TODO calcular esto
        print('TEMPORAL, BORRAME')


