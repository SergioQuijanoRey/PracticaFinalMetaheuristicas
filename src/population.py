from player import Player
import utils
from config import Config
from evals_counter import EvalsCounter

import numpy as np

class Population:
    """Representa una poblacion de jugadores (soluciones)"""

    def __init__(self, number_of_players: int, players, dimension: int):
        """Inicializa la poblacion"""
        self.number_of_players = number_of_players
        self.players = players
        self.dimension = dimension
        self.ev_counter = EvalsCounter()

        if self.is_valid() == False:
            raise Exception("Population.badInit: new population is not valid, bad initializing")

    def __len__(self):
        """Tamaño de la poblacion de jugadores"""
        return len(self.players)

    def random_population(number_of_players: int, dimension: int):
        """Genera una poblacion de jugadores inicial, aleatorios"""

        players = []
        for _ in range(number_of_players):
            player = Player.random_player(dimension)
            players.append(player)

        # Devolvemos la poblacion generada
        return Population(number_of_players, players, dimension)

    def is_valid(self):
        """Indica si una poblacion es valida o no"""

        # Tenemos un numero incorrecto de jugadores
        if self.number_of_players != len(self.players):
            return False

        # Todos los jugadores deben ser validos
        for player in self.players:
            # Este jugador no es valido
            if player.is_valid() == False:
                return False

            if player is None:
                return False

        # Todas las comprobaciones han sido superadas
        return True

    def get_best_player(self):
        """Devuelve el mejor jugador de esta poblacion"""

        # Comprobacion de seguridad
        # TODO -- no llamar a esta funcion en la version final porque hace que vaya mas lento
        if self.is_valid() == False:
            raise Exception("Population.get_best_player: population is not valid")

        # Partimos de un mejor jugador inicial
        best_player = self.players[0]
        best_fit = best_player.fitness()

        # Iteramos sobre todos los jugadores
        for player in self.players:
            curr_fit = player.fitness()

            if curr_fit < best_fit:
                best_player = player
                best_fit = curr_fit

        # Devolvemos el mejor jugador que hemos encontrado
        return best_player

    def soft_local_search_over_all_players(self, max_evals):
        """Aplica una busqueda local suave a todos los jugadores de la poblacion"""

        for player in self.players:
            # Comprobamos que no hayamos agotado todas las iteraciones
            if self.ev_counter.get_evals() >= max_evals:
                break

            player.soft_local_search(max_evals)


    def kill_closed_players(self, max_evals):
        """En cada ronda los jugadores pelean entre si. Se selecciona un jugador de forma aleatoria
        y este pelea contra un numero fijado en Config de jugadores mas cercanos a el. En el proceso,
        algunos jugadores reviven y consumen su tiempo de gracia
        """

        # No matamos a los jugadores dentro del bucle para no tener problemas con los indices fuera
        # de rango
        players_to_kill = []

        # Elegimos el primer jugador con el que vamos a pelear
        first_player_index = np.random.choice([x for x in range(len(self.players))])
        first_player = self.players[first_player_index]

        # Guardamos las distancias a este jugador
        distances_to_first_player = [
            Player.distance(first_player, player)
            for player in self.players
            if player != first_player
        ]

        # Tomamos los indices ordenados por estas distancias
        # Consideramos solo un numero de competidores segun un parametro de Config
        ordered_indexes = np.argsort(distances_to_first_player)[:Config.players_to_compete]

        # El jugador compite contra estos jugadores
        for second_index in ordered_indexes:
            # Tomamos el segundo jugador
            second_player = self.players[second_index]

            # Deben estar en el radio de vision
            if first_player.sees(second_player) == False:
                continue

            # Hacemos que peleen
            died_player_index, should_resurrect = Player.fight(first_player, second_player, first_player_index, second_index)

            # El jugador ha resucitado
            if should_resurrect is True:
                # Reaparece en una posicion aleatoria del mapa
                self.resurrect(died_player_index)

                # Intensificamos este jugador con su periodo de gracia
                self.grace_time_for_resurrecteds([died_player_index], max_evals)
            else:
                players_to_kill.append(died_player_index)


            # El jugador que muere es el primero y no resucita
            # No podemos hacer que los otros jugadores sigan compitiendo contra un jugador muerto
            if died_player_index == first_player_index and should_resurrect == False:
                break

        # Matamos a los jugadores que deben morir
        self.kill_players(players_to_kill)

    # TODO -- testear esto porque tengo dudas y puede ser critico en los algoritmos
    def kill_players(self, indexes):
        """Mata a un conjunto de jugadores, dados los indices de estos. Esto se hace en conjunto, pues
        ir matando jugador a jugador provoca que los indices de la lista se muevan y tengamos problemas
        tanto de logica como de indices fuera del rango adecuado"""

        # Primero hacemos que los jugadores muertos sean None, para marcarlos sin reducir la lista
        for dead_index in indexes:
            self.players[dead_index] = None

        # Borramos los jugadores que sean None
        self.players = [player for player in self.players if player is not None]

        # Reducimos el tamaño de la poblacion
        self.number_of_players = self.number_of_players - len(indexes)

    # TODO -- testear porque tengo dudas y puede ser critico
    def resurrect(self, index):
        """Resucita un jugador muerto. No lo elimina de la lista y lo vuelve a meter modificado,
        directamente se modifica la posicion del jugador"""
        self.players[index] = Player.random_player(self.dimension)

    def grace_time_for_resurrecteds(self, resurrected_players_indixes, max_evals):
        """
        Intensifica a los jugadores que han muerto y que han resucitado, para que puedan ser
        competitivos con el resto de jugadores

        TODO -- hacer una busqueda local dura mas inteligente

        Parameters:
        ===========
        resurrected_players_indixes: indices en la poblacion de los jugadores que han resucitado
        """
        for index in resurrected_players_indixes:
            for _ in range(Config.number_of_grace_soft_local_search):
                self.players[index].soft_local_search(max_evals)

    def remaining_players(self):
        """Calcula el porcentaje de jugadores que quedan en la poblacion respecto al numero de jugadores
        inicial"""
        return len(self.players) / Config.number_of_players

    def kill_players_outside_circle(self, circle_size, max_evals):
        """
        Los jugadores que quedan fuera del circulo mueren. Algunos de estos pueden resucitar.

        El tamaño del circulo indica el numero de veces por encima que el fitness de un jugador puede
        estar respecto el fitness del mejor jugador
        """

        # Comprobacion de seguridad
        if circle_size < 1.0:
            circle_size = 1.0

        # Tomamos el mejor jugador y su fitness
        best_player = self.get_best_player()
        best_fitness = best_player.fitness()

        # Calculamos los porcentajes respecto a este mejor fitness
        percentages = [player.fitness() / best_fitness for player in self.players]

        # Calculamos las personas que mueren
        # Tenemos hacer esto para evitar problemas con indices desactualizados al borrar elementos,
        # de la lista, y problemas con los rangos
        killed_players = []

        for idx, player in enumerate(self.players):
            if percentages[idx] > circle_size:
                # El jugador muere por estar fuera del circulo. Puede resucitar o no
                if np.random.uniform() <= Config.resurrect_prob:
                    # Resucitamos al jugador, por lo que cambia su posicion en el mapa
                    self.resurrect(idx)

                    # Intensificamos este jugador con su periodo de gracia
                    self.grace_time_for_resurrecteds([idx], max_evals)
                else:
                    killed_players.append(idx)

            # Comprobamos que tengamos mas evaluaciones del fitness
            if self.ev_counter.get_evals() >= max_evals:
                break

        # Matamos a los jugadores que deben morir
        self.kill_players(killed_players)



