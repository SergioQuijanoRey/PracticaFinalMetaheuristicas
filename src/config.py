class Config:
    """Clase en la que voy a guardar parametros globales del programa"""

    # Poblacion
    number_of_players = 50

    # Evaluaciones del fitness que tenemos por cada dimension del problema
    ev_per_dimension = 10_000

    # Porcentaje de evaluaciones que vamos a dedicar a la fase 1
    phase1_percentage = 0.6

    # Porcentaje de jugadores restantes hasta los que esperamos en la fase 1
    phase1_players_percentage = 0.5

    # Busqueda local suave
    tries_in_local_search = 2
    step_size = 10.0

    # Peleas de jugadores
    player_radius_vision_per_dimension = 50
    players_to_compete = 4
    best_player_survives_prob = 0.90
    resurrect_prob = 0.05
    number_of_grace_soft_local_search = 5
