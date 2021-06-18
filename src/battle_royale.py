import numpy as np
import cec17 as api
from population import Population
from player import Player
from config import Config
from evals_counter import EvalsCounter
import utils

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

        # Condiciones para permanecer en la fase 1 de la partida
        phase1_iterations_cond = ev_counter.get_evals() < self.max_evals() * Config.phase1_percentage
        phase1_number_of_players_cond = self.population.remaining_players() >= Config.phase1_players_percentage
        pase1_condition = phase1_iterations_cond and phase1_number_of_players_cond

        while pase1_condition:

            print("TODO -- busqueda local sobre todos los jugadores")
            # Aplicamos una busqueda suave sobre cada jugador
            self.population.soft_local_search_over_all_players()

            print("TODO -- matamos jugadores cercanos")
            # Ronda de asesinatos entre jugadores iniciales
            # En el proceso, algunos jugadores mueren y resucitan. En esta funcion, estos jugadores
            # resucitados consumen su tiempo de gracia
            resurrected_players_indixes = self.population.kill_closed_players()

            print(f"TODO -- Hemos consumido {ev_counter.get_evals()} iteraciones")
            print(f"TODO -- tenemos una poblacion de {len(self.population.players)} jugadores")
            utils.wait_for_user_input()



        #  print("--> Fase 2")
        #  while evals < self.max_evals():
        #      # Los jugadores fuera del circulo mueren
        #      self.population.kill_players_outside_circle()

        #      # Algunos de los jugadores fuera del circulo reviven

        print("TODO -- acabada la partida")
        # Devolvemos el mejor jugador
        return self.population.get_best_player()
