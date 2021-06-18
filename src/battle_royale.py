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
        # Escribimos las condiciones en lambdas para mayor expresividad y para que en cada iteracion
        # del bucle se vuelva a comprobar la condicion
        phase1_iterations_cond = lambda: ev_counter.get_evals() < self.max_evals() * Config.phase1_percentage
        phase1_number_of_players_cond = lambda:  self.population.remaining_players() >= Config.phase1_players_percentage
        pase1_condition = lambda: phase1_iterations_cond() and phase1_number_of_players_cond()

        while pase1_condition():

            # Aplicamos una busqueda suave sobre cada jugador
            self.population.soft_local_search_over_all_players(self.max_evals())

            # Si hemos agotado las iteraciones, paramos
            if ev_counter.get_evals() >= self.max_evals():
                break

            # Ronda de asesinatos entre jugadores iniciales
            # En el proceso, algunos jugadores mueren y resucitan. En esta funcion, estos jugadores
            # resucitados consumen su tiempo de gracia
            resurrected_players_indixes = self.population.kill_closed_players(self.max_evals())

        print("--> Fase 2")

        circle_size = Config.init_circle_size

        while ev_counter.get_evals() < self.max_evals():
            # Los jugadores fuera del circulo mueren
            # En este proceso, alguno de los jugadores reviven
            self.population.kill_players_outside_circle(circle_size, self.max_evals())

            # Comprobamos que no hayamos consumido todas las evaluaciones
            if ev_counter.get_evals() >= self.max_evals():
                break

            # Los jugadores se mueven algo
            # TODO -- no iterar sobre todos los jugadores
            self.population.soft_local_search_over_all_players(self.max_evals())

            # Hacemos mas cerrado el circulo
            circle_size += Config.circle_step

            # Si solo queda un jugador, paramos de iterar
            if len(self.population) == 1:
                break

        # Devolvemos el mejor jugador
        return self.population.get_best_player()
