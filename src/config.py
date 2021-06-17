class Config:
    """Clase en la que voy a guardar parametros globales del programa"""

    # Poblacion
    number_of_players = 1000

    # Evaluaciones del fitness que tenemos por cada dimension del problema
    ev_per_dimension = 10_000

    # Porcentaje de evaluaciones que vamos a dedicar a la fase 1
    phase1_percentage = 0.6

    # Busqueda local suave
    tries_in_local_search = 2
    step_size = 10.0
