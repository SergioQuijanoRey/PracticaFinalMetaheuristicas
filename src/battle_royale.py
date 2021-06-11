import numpy as np

class BattleRoyale:
    """Clase que representa la metaheuristica que desarrollamos"""

    def __init__(self, dimension, ev_per_dimension):
        self.dimension = dimension
        self.ev_per_dimension = ev_per_dimension

    def search(self):
        best_solution = Player.random_player(self.dimension)

        evals = 0
        while evals < self.dimension * self.ev_per_dimension:
            print("..", end=" - ")
            evals += 1000
        print("")

        return best_solution

class Popuation:
    """Representa una poblacion de jugadores (soluciones)"""
    def __init__(self):
        pass


# Constantes asociadas a las funciones con las que trabajamos
#===============================================================================
lower_range = -100
upper_range = 100

class Player:
    """Clase que representa un jugador (solucion) al problema considerado"""

    def __init__(self, dimension, genes):
        self.dimension = dimension
        self.genes = genes

        if self.is_valid() == False:
            raise Exception("Player.BadInit: new solution is not valid, bad initializing")

    def random_player(dimension):
        """Genera un jugador con genes aleatorios"""
        genes = np.random.randint(lower_range, upper_range, dimension)
        rand_player = Player(dimension, genes)
        return rand_player

    def is_valid(self):
        """
        Comprueba que el jugador represente una solucion valida
        Returns:
        ========
        true: si el jugador es valido
        false: si el jugador no es valido
        """

        # El tamaño del vector solucion debe coincidir con el tamaño especificado
        if len(self.genes) != self.dimension:
            return False

        # Los genes estan en el rango permitido para las funciones con las que trabajamos
        for gene in self.genes:
            if gene < lower_range or gene > upper_range:
                return False

        # Todas las comprobaciones han sido superadas
        return True

    def to_list(self):
        """
        Convierte el jugador en una lista de python, para poder ser usada en funciones de la api que
        nos dan los profesores de practicas.
        """
        return self.genes.tolist()

    def fitness(self):
        """Devuelve el fitness asociado a este jugador"""
        pass


