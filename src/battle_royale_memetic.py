from battle_royale import BattleRoyale

class BattleRoyaleMemetic(BattleRoyale):
    """
    Incluiremos una mejora memetica en la que usaremos la busqueda local solis para la hibridacion

    Notar que inicialmente estabamos usando una busqueda local muy suave para hacer que los jugadores
    se moviesen por el mapa. Pero sin caer exactamente en un modelo que se basase fuertemente en la
    busqueda local, sino que nos basabamos mas en el mecanismo de jugadores matandose, jugadores muriendo
    por el cerrado del circulo y jugadores resucitando para dar variedad a la poblacion

    TODO -- indicar donde vamos a aplicar la busqueda local fuerte
    Aplicaremos la busqueda local fuerte sobre TODO

    Solo tenemos que modifcar el metodo que corre la partida
    """
    def run_game(self):
        """
        Comienza una partida y devuelve al jugador ganador.

        Returns:
        ========
        best_player: el jugador que gana la partida
        """

        # TODO -- borrar los mensajes por pantalla porque pueden relantecer la ejecucion
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
