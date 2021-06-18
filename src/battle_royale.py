import numpy as np
import cec17 as api
from population import Population
from player import Player
from config import Config
from evals_counter import EvalsCounter

class BattleRoyale:
    """Clase que representa la metaheuristica que desarrollamos.
    Es necesario que antes de usar esta clase se haya fijado la funcion con la que trabajamos con
    la funcion cec17.init
    """

    def __init__(self, dimension, number_of_players):
        self.dimension = dimension
        self.population = None
        self.number_of_players = number_of_players

    def dummy_search(self):
        """Devuelve un jugador aleatorio.
        Con fines de debuggear nuestro codigo
        """
        best_solution = Player.random_player(self.dimension)

        evals = 0
        while evals < self.dimension * self.ev_per_dimension:
            evals += 1000
        print("")

        return best_solution

    def max_evals(self):
        """Calcula el maximo de evaluaciones del fitness que se pueden consumir"""
        return self.dimension * Config.ev_per_dimension


    def run_game(self):
        """Comienza una partida y devuelve al jugador ganador.

        Returns:
        ========
        best_player: el jugador que gana la partida

        TODO -- borrar los mensajes por pantalla porque pueden relantecer la ejecucion
        """

        # Controlamos las evaluaciones que nos quedan
        ev_counter = EvalsCounter()
        ev_counter.reset()

        print("--> Fase inicial: generando jugadores en posiciones aleatorias")
        self.population = Population.random_population(self.number_of_players, self.dimension)

        print("--> Fase 1")
        while ev_counter.get_evals() < self.max_evals() * Config.phase1_percentage:
            # Aplicamos una busqueda suave sobre cada jugador
            self.population.soft_local_search_over_all_players()

            # Ronda de asesinatos entre jugadores iniciales
            # Se devuelven los indices en la poblacion de los jugadores que han resucitado, para
            # poder intensificarlos mas tarde
            resurrected_players_indixes = self.population.kill_closed_players()

            # Ronda de intensificacion para los jugadores revividos
            self.population.grace_time_for_resurrecteds(resurrected_players_indixes)


        #  print("--> Fase 2")
        #  while evals < self.max_evals():
        #      # Los jugadores fuera del circulo mueren
        #      self.population.kill_players_outside_circle()

        #      # Algunos de los jugadores fuera del circulo reviven

        # Devolvemos el mejor jugador
        return self.population.get_best_player()
