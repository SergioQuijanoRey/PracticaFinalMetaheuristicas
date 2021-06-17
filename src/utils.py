
# Controla si queremos parar la ejecucion o no con la siguiente funcion
WAIT = True

def wait_for_user_input(msg = "Pulse una tecla para CONTINUAR..."):
    """Espera a que el usuario pulse una tecla para continuar la ejecucion"""
    input(msg)
