import numpy as np
import cec17

if __name__ == "__main__":
    print("==> Inicializamos la semilla aleatoria")
    np.random.seed(123456789)

    # Evaluaciones del fitness que tenemos por cada dimension del problema
    ev_per_dimension = 10000

    # Dimension del problema con el que trabajamos
    dimension = 10

    # Lanzamos todas las funciones
    for function_id in range(1, 31):
        # Evaluaciones del fitness consumidas hasta el momento
        evals = 0

        # Fijamos la funcion a utilizar en esta iteracion
        cec17.init("pruebas", function_id, dimension);

        # Para mostrar los mensajes por pantalla
        cec17.print_output();

        # Iteramos mientras no hayamos consumido las evaluaciones
        while evals < dimension * ev_per_dimension:
            print("..", end=" - ")
            evals += 1000
        print("")

    # Mostramos el error alcanzando
    err = cec17.fitness(np.zeros(dimension), dimension)
    print(f"Error alcanzado: {err}")
