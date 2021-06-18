from player import Player
import utils
from config import Config

class Population:
    """Representa una poblacion de jugadores (soluciones)"""

    def __init__(self, number_of_players: int, players, dimension: int):
        """Inicializa la poblacion"""
        self.number_of_players = number_of_players
        self.players = players
        self.dimension = dimension

        if self.is_valid() == False:
            raise Exception("Population.badInit: new population is not valid, bad initializing")

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

    def soft_local_search_over_all_players(self):
        """Aplica una busqueda local suave a todos los jugadores de la poblacion"""

        # TODO -- hay que comprobar que no hayamos agotado todas las iteraciones
        for player in self.players:
            player.soft_local_search()

    def kill_closed_players(self):
        """Los jugadores que estan cerca unos de otros luchan

        Returns:
        ========
        resurrected_players_indixes: indices en la poblacion de los jugadores que han muerto y que
                                     han resucitado

        TODO -- da problemas a la hora de matar a los jugadores porque se va moviendo la lista
        """

        # Jugadores que deben revivir
        # No revivimos a los jugadores dentro del bucle para no tener problemas con los indices
        # fuear de rango
        resurrected_players_indixes = []

        # No matamos a los jugadores dentro del bucle para no tener problemas con los indices fuera
        # de rango
        players_to_kill = []

        for first_index, first_player in enumerate(self.players):
            for second_index, second_player in enumerate(self.players):
                if first_player != second_player and Player.distance(first_player, second_player) < Config.player_radius_vision:
                    # Hacemos que peleen
                    died_player_index, should_resurrect = Player.fight(first_player, second_player, first_index, second_index)

                    if should_resurrect:
                        # Añadimos el indice a los jugadores qwue deben resucitar
                        resurrected_players_indixes.append(died_player_index)
                    else:
                        # Añadimos a la lista de jugadores a borrar
                        players_to_kill.append(died_player_index)

        # Resucitamos a los jugadores
        for resurrected_player in resurrected_players_indixes:
            self.resurrect(resurrected_player)

        # Matamos a los jugadores que deben morir
        for died_player in players_to_kill:
            self.kill_player(died_player)

        return resurrected_players_indixes

    def kill_player(self, index):
        """Mata a un jugador, borrandolo de la poblacion de jugadores"""
        print(f"TODO -- queremos eliminar el indice {index}, tenemos {len(self.players)} jugadores")
        self.players.pop(index)

    def resurrect(self, index):
        """Resucita un jugador muerto. No lo elimina de la lista y lo vuelve a meter modificado,
        directamente se modifica la posicion del jugador"""
        self.players[index] = Player.random_player(self.dimension)

    def grace_time_for_resurrecteds(self, resurrected_players_indixes):
        """
        Intensifica a los jugadores que han muerto y que han resucitado, para que puedan ser
        competitivos con el resto de jugadores

        Parameters:
        ===========
        resurrected_players_indixes: indices en la poblacion de los jugadores que han resucitado
        """
        pass
