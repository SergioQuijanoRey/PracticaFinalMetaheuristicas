from player import Player

class Population:
    """Representa una poblacion de jugadores (soluciones)"""

    def __init__(self, pop_size, dimension, players = []):
        """Inicializa la poblacion"""
        self.pop_size = pop_size
        self.players = players
        self.dimension = dimension

        if self.is_valid() == False:
            raise Exception("Population.badInit: new population is not valid, bad initializing")

    def random_population(number_of_players, dimension):
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
        if self.pop_size != len(self.players):
            return False

        # Todos los jugadores deben ser validos
        for player in self.players:
            # Este jugador no es valido
            if player.is_valid() == False:
                return False

        # Todas las comprobaciones han sido superadas
        return True
