from player import Player
import utils

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
        """Devuelve el mejor jugador de esta poblacion, junto a las evaluaciones del fitness que se consumen"""

        # Comprobacion de seguridad
        # TODO -- no llamar a esta funcion en la version final porque hace que vaya mas lento
        if self.is_valid() == False:
            raise Exception("Population.get_best_player: population is not valid")

        # Partimos de un mejor jugador inicial
        best_player = self.players[0]
        best_fit, ev_cons = best_player.fitness()
        fit_ev_cons = ev_cons

        # Iteramos sobre todos los jugadores
        for player in self.players:
            curr_fit, ev_cons = player.fitness()
            fit_ev_cons += ev_cons

            if curr_fit < best_fit:
                best_player = player
                best_fit = curr_fit

        # Devolvemos el mejor jugador que hemos encontrado, y las iteraciones consumidas
        return best_player, fit_ev_cons

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
        """
        pass

    def grace_time_for_resurrecteds(self, resurrected_players_indixes):
        """
        Intensifica a los jugadores que han muerto y que han resucitado, para que puedan ser
        competitivos con el resto de jugadores

        Parameters:
        ===========
        resurrected_players_indixes: indices en la poblacion de los jugadores que han resucitado
        """
        pass
