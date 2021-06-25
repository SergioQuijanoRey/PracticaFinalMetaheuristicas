import cec17 as api
import numpy as np
from config import Config
from evals_counter import EvalsCounter
import solis

class Player:
    """Clase que representa un jugador (solucion) al problema considerado"""

    def __init__(self, dimension, position):
        self.dimension = dimension
        self.position = position

        # Cuando el fitness es None, significa que no lo hemos calculado
        # Cuando el fitness no es None, significa que no lo hemos calculado. Asi que cada vez que
        # mutemos un jugador, debemos anular este valor cacheado
        self.fitness_cache = None

        self.ev_counter = EvalsCounter()

        if self.is_valid() == False:
            raise Exception("Player.BadInit: new solution is not valid, bad initializing")

    def random_player(dimension):
        """Genera un jugador en una posicion aleatoria"""
        position = np.random.randint(Config.lower_range, Config.upper_range, dimension)
        rand_player = Player(dimension, position)
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
        if len(self.position) != self.dimension:
            return False

        # La posicion esta en un rago valido
        for coordinate in self.position:
            if coordinate < Config.lower_range or coordinate > Config.upper_range:
                return False

        # Todas las comprobaciones han sido superadas
        return True

    def to_list(self):
        """
        Convierte el jugador en una lista de python, para poder ser usada en funciones de la api que
        nos dan los profesores de practicas.
        """
        return self.position.tolist()

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
        self.calculate_fitness()
        return self.fitness_cache

    def calculate_fitness(self):
        """Calcula el fitness de este jugador. Para ello, self.fitness no debe estar cacheado"""

        # Comprobacion de seguridad
        if self.fitness_cache is not None:
            raise Exception("Player.calculate_fitness: self.fitness is not None")

        # Aumentamos las evaluaciones consumidas
        self.ev_counter.add_evals(1)

        # Realizamos el calculo y lo guardamos
        self.fitness_cache = api.fitness(self.to_list(), self.dimension)

    def soft_local_search(self, max_evals):
        """Aplica una busqueda local suave, lo que hace que el jugador se mueva a una posicion mejor.

        La busqueda local suave considerada genera un numero determinado en Config de posiciones a
        modificar. Se considera un cambio aleatorio positivo y otro negativo, en el rango [0, alpha]
        donde alpha se determina en Config
        """

        best_player = self
        best_fitness = self.fitness()

        for _ in range(Config.tries_in_local_search):
            # Posicion y valor de variacion de la coordenada
            position = np.random.randint(0, len(self.position))
            delta = np.random.uniform(-Config.step_size, Config.step_size)

            # Modificamos la posicion
            new_position = self.position.copy()
            new_position[position] = new_position[position] + delta

            # Generamos el nuevo jugador
            # Si el jugador no es valido, lo ignoramos
            new_player = None
            try:
                new_player = Player(self.dimension, new_position)
            except:
                continue

            # Comprobamos si es mejor que el mejor jugador hasta el momento
            new_pla_fit = new_player.fitness()
            if new_pla_fit < best_fitness:
                best_player = new_player
                best_fitnes = new_pla_fit

            # Comprobamos si tenemos que parar de buscar por haber agotado las iteraciones
            if self.ev_counter.get_evals() >= max_evals:
                break

        # Hacemos el cambio mas optimo
        # Notar que no tenemos que invalidar la cache. best_player ha calculado su fitness
        # correspondiente, que es el que tomamos ahora como nuestro
        self = best_player

    def hard_local_search(self, max_evals, ignore_config_threshold = False):
        """
        Aplicamos una busqueda local fuerte sobre este jugador

        Parameters:
        ===========
        max_evals: las evaluaciones del fitness maximas
        ignore_config_threshold: se consume el maximo de evaluaciones ignorando el tope dado en la
                                 configuracion. Util para la ultima busqueda sobre el mejor jugador
                                 en el algoritmo memetico
        """

        # Tomamos el minimo entre estos dos maximos de evaluaciones
        if ignore_config_threshold == False:
            max_local_evals = min(Config.max_evals_hard_local_search, max_evals - self.ev_counter.get_evals())
        else:
            max_local_evals = max_evals - self.ev_counter.get_evals() - 100

        # Corremos esta busqueda local fuerte
        result, _ = self.position = solis.soliswets(
            # Usamos una lambda para seguir el formato de funcion que espera solis
            # Necesita una funcion que dadas unas coordenadas, devuelva el fitness. Como necesitamos
            # pasar la dimension, la fijamos usando una closure
            lambda coordinates: api.fitness(coordinates, self.dimension),

            self.position,
            self.fitness(),
            Config.lower_range,
            Config.upper_range,
            max_local_evals,
            np.full(self.dimension, Config.delta)
        )

        # Tomamos los resultados de la busqueda local
        self.position = result.solution
        self.fitness_cache = result.fitness

        # Aumentamos las iteraciones consumidas, porque solis no hace que aumenten pues usa directamente
        # la funcion de api.fitness
        self.ev_counter.add_evals(result.evaluations)


    def invalidate_cache(self):
        """Se invalida la cache del fitness"""
        self.fitness = None

    # TODO -- testear porque es sencillo y critico
    def distance(first_player, second_player):
        """Devuelve la distancia entre dos jugadores.
        Estamos usando la distancia manhattan por temas de eficiencia
        """
        return np.sum(np.abs(first_player.position - second_player.position))

    def fight(first_player, second_player, first_index, second_index):
        """Dos jugadores pelean, uno de los dos mueren

        El jugador con mejor fitness sobrevive la mayoria de veces. Segun una pequeña probabilidad,
        el peor jugador puede sobrevivir

        El jugador que muere tiene una probabilidad de resucitar

        Returns:
        ========
        died_player_index: int, indice del jugador que muere
        should_resurrect: bool, indica si el jugador que muere debe resucitar
        """

        # Seleccionamos el mejor y peor indice de los jugadores
        if first_player.fitness() < second_player.fitness():
            best_index = first_index
            worst_index = second_index
        else:
            worst_index = first_index
            best_index = second_index

        # Segun la probabilidad, el mejor jugador o el peor jugador sobreviven
        if np.random.uniform() < Config.best_player_survives_prob:
            died_player_index = worst_index
        else:
            died_player_index = best_index

        # El jugador muerto debe sobrevivir?
        if np.random.uniform() < Config.resurrect_prob:
            should_resurrect = True
        else:
            should_resurrect = False

        return died_player_index, should_resurrect

    def sees(self, other_player) -> bool:
        """Comprueba si otro jugador esta en el radio de vision de este jugador"""
        return Player.distance(self, other_player) <= Config.player_radius_vision_per_dimension * self.dimension


    def __str__(self):
        """Para hacer un buen print de estos objetos"""
        result = ""
        result += "Player:\n"
        result += f"\t-> Position: {self.position} \n"
        result += f"\t-> Fitness: {self.fitness_cache}"
        return result


