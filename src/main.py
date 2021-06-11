import numpy as np
import cec17
from battle_royale import BattleRoyale, Player

if __name__ == "__main__":
    print("==> Inicializamos la semilla aleatoria")
    np.random.seed(123456789)

    # Evaluaciones del fitness que tenemos por cada dimension del problema
    ev_per_dimension = 10_000

    # Dimension del problema con el que trabajamos
    dimension = 10

    # Lanzamos todas las funciones
    for function_id in range(1, 31):
        # Evaluaciones del fitness consumidas hasta el momento
        evals = 0

        # Fijamos la funcion a utilizar en esta iteracion
        # Con ello, el resto de llamadas cec17 usan los datos de la funcion especificada (en particular,
        # el fitness)
        cec17.init("pruebas", function_id, dimension);

        # Para mostrar los mensajes por pantalla
        cec17.print_output();

        # Inicalizamos nuestra metaheuristica
        mh = BattleRoyale(dimension = dimension, ev_per_dimension = ev_per_dimension)

        # Tomamos la solucion a partir de la busqueda
        best_player = mh.search()

    # Mostramos el error alcanzando
    err = cec17.fitness(best_player.to_list(), dimension)
    print(f"Error alcanzado: {err}")
