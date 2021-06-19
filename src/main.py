import numpy as np
import cec17
from battle_royale import BattleRoyale
from battle_royale_memetic import BattleRoyaleMemetic
from player import Player
from config import Config
import sys

def get_program_parameters():
    """Toma los parametros de entrada por linea de comandos"""

    if len(sys.argv) != 3:
        print("Parametros de entrada invalidos")
        show_help()
        exit(-1)

    if sys.argv[2] == "standar":
        resurrect_hard_local_search = False
    elif sys.argv[2] == "memetic":
        resurrect_hard_local_search = True
    else:
        print("El argumento que indica la metaheuristica nos es valido")
        show_help()
        exit(-1)

    return int(sys.argv[1]), resurrect_hard_local_search

def show_help():
    """Mostramos como se usa en programa"""
    print("Modo de uso:")
    print("\tpython3 main.py <dimension> <version>")
    print("\tversion: standar | memetic")

if __name__ == "__main__":
    # Tomamos los parametros por linea de comandos
    dimension, hard_local_search = get_program_parameters()

    print("==> Inicializamos la semilla aleatoria")
    np.random.seed(123456789)

    # Lanzamos todas las funciones
    for function_id in range(1, 31):
        # Fijamos la funcion a utilizar en esta iteracion
        # Con ello, el resto de llamadas cec17 usan los datos de la funcion especificada (en particular,
        # el fitness)
        cec17.init("battle_royale", function_id, dimension);

        # Para mostrar los mensajes por pantalla
        #  cec17.print_output()

        # Inicalizamos nuestra metaheuristica segun el parametro dado por el usuario
        if hard_local_search == False:
            mh = BattleRoyale(dimension = dimension, number_of_players = Config.number_of_players)
        else:
            mh = BattleRoyaleMemetic(dimension = dimension, number_of_players = Config.number_of_players)

        # Tomamos la solucion a partir de la busqueda
        best_player = mh.run_game()

        # Mostramos el error alcanzando para esta funcion
        err = cec17.fitness(best_player.to_list(), dimension)
        print(f"Funcion {function_id},\terror: {err}")

