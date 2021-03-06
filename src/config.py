class Config:
    """Clase en la que voy a guardar parametros globales del programa"""

    # Rangos de las funciones
    lower_range = -100
    upper_range = 100

    # Poblacion
    number_of_players = 20_000

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
    resurrect_prob = 0.5
    number_of_grace_soft_local_search = 5

    # Cerrado del circulo
    init_circle_size = 5.0
    circle_step = -0.1

    # Busqueda fuerte
    max_evals_hard_local_search = 375
    delta = 0.15
