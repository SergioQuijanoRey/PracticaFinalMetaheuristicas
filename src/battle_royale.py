import numpy as np
import cec17 as api
from population import Population
from player import Player

class BattleRoyale:
    """Clase que representa la metaheuristica que desarrollamos.
    Es necesario que antes de usar esta clase se haya fijado la funcion con la que trabajamos con
    la funcion cec17.init
    """

    def __init__(self, dimension, ev_per_dimension, number_of_players):
        self.dimension = dimension
        self.ev_per_dimension = ev_per_dimension
        self.population = None
        self.number_of_players = number_of_players

    def dummy_search(self):
        """Devuelve un jugador aleatorio.
        Con fines de debuggear nuestro codigo
        """
        best_solution = Player.random_player(self.dimension)

        evals = 0
        while evals < self.dimension * self.ev_per_dimension:
            print("..", end=" - ")
            evals += 1000
        print("")

        return best_solution

    def max_evals(self):
        """Calcula el maximo de evaluaciones del fitness que se pueden consumir"""
        return self.dimension * self.ev_per_dimension


    def run_game(self):
        """Comienza una partida y devuelve al jugador ganador."""

        # Parametros iniciales
        evals = 0
        best_player = None

        # Creamos una poblacion de jugadores inicial
        evals = 0
        while evals < self.max_evals():
            self.population = Population.random_population(self.number_of_players, self.dimension)
            best_player, cons_evals = self.population.get_best_player()
            evals += cons_evals

        return best_player
