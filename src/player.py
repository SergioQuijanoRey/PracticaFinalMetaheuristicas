import cec17 as api
import numpy as np

# Constantes asociadas a las funciones con las que trabajamos
#===============================================================================
lower_range = -100
upper_range = 100

class Player:
    """Clase que representa un jugador (solucion) al problema considerado"""

    def __init__(self, dimension, genes):
        self.dimension = dimension
        self.genes = genes

        # Cuando el fitness es None, significa que no lo hemos calculado
        # Cuando el fitness no es None, significa que no lo hemos calculado. Asi que cada vez que
        # mutemos un jugador, debemos anular este valor cacheado
        self.fitness = None

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
        """Devuelve el fitness asociado a este jugador.

        Returns:
        ========
        fitness: valor del fitness del jugador
        ev_cons: evaluaciones del fitness consumidas (0 o 1)
        """

        # El valor del fitness esta cacheado, no tenemos que recalcularlo
        if self.fitness is not None:
            return self.fitness, 0

        else:
            self.calculate_fitness()
            return self.fitness, 1

    def calculate_fitness(self):
        """Calcula el fitness de este jugador. Para ello, self.fitness no debe estar cacheado"""

        # Comprobacion de seguridad
        if self.fitness is not None:
            raise Exception("Player.calculate_fitness: self.fitness is not None")

        # Realizamos el calculo y lo guardamos
        self.fitness = api.fitness(self.to_list(), self.dimension)

