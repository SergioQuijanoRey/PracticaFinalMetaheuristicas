import cec17 as api
import numpy as np
from config import Config
from evals_counter import EvalsCounter

# Constantes asociadas a las funciones con las que trabajamos
#===============================================================================
lower_range = -100
upper_range = 100

class Player:
    """Clase que representa un jugador (solucion) al problema considerado"""

    def __init__(self, dimension, genes):
        self.dimension = dimension
        # TODO -- renombrar por position
        self.genes = genes

        # Cuando el fitness es None, significa que no lo hemos calculado
        # Cuando el fitness no es None, significa que no lo hemos calculado. Asi que cada vez que
        # mutemos un jugador, debemos anular este valor cacheado
        self.fitness_cache = None

        self.ev_counter = EvalsCounter()

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
        """

        # El valor del fitness esta cacheado, no tenemos que recalcularlo
        # No aumentamos el numero de iteraciones
        if self.fitness_cache is not None:
            return self.fitness_cache

        # Calculamos el valor del fitness
        # Aumentamos las evaluaciones consumidas
        self.ev_counter.add_evals(1)
        self.calculate_fitness()
        return self.fitness_cache,

    def calculate_fitness(self):
        """Calcula el fitness de este jugador. Para ello, self.fitness no debe estar cacheado"""

        # Comprobacion de seguridad
        if self.fitness_cache is not None:
            raise Exception("Player.calculate_fitness: self.fitness is not None")

        # Realizamos el calculo y lo guardamos
        self.fitness_cache = api.fitness(self.to_list(), self.dimension)

    def soft_local_search(self):
        """Aplica una busqueda local suave, lo que hace que el jugador se mueva a una posicion mejor.

        La busqueda local suave considerada genera un numero determinado en Config de posiciones a
        modificar. Se considera un cambio aleatorio positivo y otro negativo, en el rango [0, alpha]
        donde alpha se determina en Config

        TODO -- llevar la cuenta de las iteraciones consumidas
        """

        best_player = self
        for _ in range(Config.tries_in_local_search):
            # Posicion y valor de variacion de la coordenada
            position = np.random.randint(0, len(self.genes))
            delta = np.random.uniform(-Config.step_size, Config.step_size)

            # Modificamos los genes
            # TODO -- es necesario hacer copy() ??
            new_genes = self.genes.copy()
            new_genes[position] = new_genes[position] + delta

            # Generamos el nuevo jugador
            # Si el jugador no es valido, lo ignoramos
            # TODO -- esto hacerlo con mas cuidado. Jugadores en el borde no se pueden acercar bien
            # al borde
            new_player = None
            try:
                new_player = Player(self.dimension, new_genes)
            except:
                continue

            # Comprobamos si es mejor que el mejor jugador hasta el momento
            if new_player.fitness() < best_player.fitness():
                best_player = new_player

        # Hacemos el cambio mas optimo
        # Notar que no tenemos que invalidar la cache. best_player ha calculado su fitness
        # correspondiente, que es el que tomamos ahora como nuestro
        self = best_player

    def invalidate_cache(self):
        """Se invalida la cache del fitness"""
        self.fitness = None


    def __str__(self):
        """Para hacer un buen print de estos objetos"""
        result = ""
        result += "Player:\n"
        result += f"\t-> Position: {self.genes} \n"
        result += f"\t-> Fitness: {self.fitness}"
        return result


