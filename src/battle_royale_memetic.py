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

    Solo tenemos que modifcar el inicializador para hacer self.memetic == True. En la version base de
    la clase tenemos toda la logica que incluye el comportamiento memetico
    """

    def __init__(self, dimension, number_of_players):
        self.dimension = dimension
        self.population = None
        self.number_of_players = number_of_players

        # En esta version si que usamos la busqueda local fuerte para las resurrecciones
        self.memetic = True
