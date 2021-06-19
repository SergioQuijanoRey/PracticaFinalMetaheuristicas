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

def parameter_tuning():
    """
    Funcion que hemos usado para ir variando algunos parametros de la configuracion en busca en busca
    de los mejores valores para los parametros

    Por el coste computacional, solo usamos la dimension 10 para tomar las decisiones, lo que puede
    no ser optimo. En vez de hacer grid search, hacemos un coordinate descent: fijamos un parametro y
    moviendolo buscamos el optimo. Esto puede ser un proceso tampoco optimo pero mas ligero computacionalmente

    Los distintos parametros con los que hemos probado han sido, en orden:
        - number_of_players: 500, 1000, 5000, 10000, 20000, 25000 <- Ganador: 25k pero es demasiado
                                                                     lento, asi que nos quedamos con
                                                                     20k
        - resurrect_prob: 0.05, 0.1 <- Ganador:
    """

    # Tomamos los parametros por linea de comandos
    dimension, hard_local_search = get_program_parameters()
    np.random.seed(123456789)

    # Primera configuruacion
    Config.resurrect_prob = 0.1

    first_config_error = []
    for function_id in range(1, 31):
        cec17.init("battle_royale", function_id, dimension);
        if hard_local_search == False:
            mh = BattleRoyale(dimension = dimension, number_of_players = Config.number_of_players)
        else:
            mh = BattleRoyaleMemetic(dimension = dimension, number_of_players = Config.number_of_players)
        best_player = mh.run_game()
        err = cec17.fitness(best_player.to_list(), dimension)
        print(f"Funcion {function_id},\terror: {err}")

        # Añadimos el error a la primera funcion
        first_config_error.append(err)

    # Segunda configuracion:
    Config.resurrect_prob = 0.5

    second_config_error = []
    for function_id in range(1, 31):
        cec17.init("battle_royale", function_id, dimension);
        if hard_local_search == False:
            mh = BattleRoyale(dimension = dimension, number_of_players = Config.number_of_players)
        else:
            mh = BattleRoyaleMemetic(dimension = dimension, number_of_players = Config.number_of_players)
        best_player = mh.run_game()
        err = cec17.fitness(best_player.to_list(), dimension)
        print(f"Funcion {function_id},\terror: {err}")

        # Añadimos el error a la primera funcion
        second_config_error.append(err)

    # Comparamos los resultados
    print(f"Media del error en la primera configuracion: {np.mean(first_config_error)}")
    print(f"Media del error en la segunda configuracion: {np.mean(second_config_error)}")
    print(f"Error Primero / Error Segundo:\n{np.array(first_config_error) / np.array(second_config_error)}")
    print(f"Media del vector Error Primero / Error Segundo: {np.mean(np.array(first_config_error) / np.array(second_config_error))}")

    # Salimos para que no se ejecute el programa normal
    exit(-1)


if __name__ == "__main__":
    # TODO -- comentar esta funcion
    # Esta funcion esta comentada porque el parameter tuning ya ha sido realizado
    parameter_tuning()

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

