# Práctica Final Metaheurísticas

* Repositorio para alojar el código de la práctica final, alternativa al examen de la asignatura
* Metaheurística original basada en los juegos tipo *Battle Royale*

# Planteamiento de la metaheuristica

Como inspiración voy a considerar el nuevo género de videojuegos llamado *Battle Royal*. Estos videojuegos se parecen mucho a la serie de libros "Los juegos del hambre".

En estos videojuegos, una serie de jugadores (entre 50 y 100) se reparten a lo largo de un mapa. El objetivo es ser el último jugador vivo durante la partida. Para ello, tienen que seguir una serie de dinámicas durante la partida:

1. Al principio de la partida, deben recolectar armas y otros recursos, porque todos los jugadores aparecen en el mapa sin equipación
    * Esto puede verse reflejado en la metaheurística como una primera búsqueda local, muy suave, aplicada a las soluciones iniciales aleatorias
2. Deben matar / defenderse de los otros jugadores con los que se pueden encontrar a través del mapa
    * He pensado que, para reflejar esto, si dos soluciones están muy cerca la una de la otra, la solución mejor *mate* a la solución peor con cierta probabilidad (en el juego, puedes ir mejor equipado, pero perder el duelo por ser un jugador menos habilidoso). Soluciones muy cerca en el sentido en el que la distancia euclídea de los vectores que representan las dos soluciones estén por debajo de un valor dado
3. A partir de cierto tiempo, el mapa se cierra incrementalmente sobre un área circular del mapa, cada vez más pequeña. Con esto se fomenta que los jugadores tengan que enfrentarse unos con otros, y potenciando que los jugadores mejor equipados y más habilidosos ganen sin tener que esperar demasiado tiempo a malos jugadores escondidos por el mapa
    * Para representar esto en la metaheurística, a partir de cierta iteración, se realizarán eliminaciones de la población. A partir de este momento, cada cierto número de iteraciones, los $\lambda$ peores elementos de la población, son eliminados al quedar fuera del círculo
4. Hay una cierta probabilidad de revivir si te matan, aunque no es muy alta. Cuando revives, reapareces sin nada de lo que habías estado recolectando durante la partida. Se otorga un periodo de inmunidad en el que el jugador que ha revivido tiene que recolectar rápidamente recursos para ser competitivo contra jugadores que van más avanzados en la partida. Además, puede ser que reaparezcan fuera del círculo, luego deben lograr entrar al círculo en el tiempo de gracia
    * Por tanto, si un jugador muere, tiene una probabilidad dada (potencialmente baja) de revivir
    * Al revivir, pierde todos sus recursos. Esto se materializa en que se le asigna una solución aleatoria
    * El periodo de gracia se materializa en que dispondrá de un número de iteraciones de alguna búsqueda, por ejemplo, búsqueda local, para intentar ser competitivo con el resto de soluciones que llevan toda la partida mejorando su fitness
    * Decido también que, si un jugador muere contra el mejor jugador hasta el momento, revive siempre. Esto no se aplica cuando quedan menos de un número dado de jugadores (fase final de la partida)

Además de esto, consideramos algunos aspectos generales a todas las metaheurísticas vistas en clase:

* En las distintas iteraciones, realizaremos una búsqueda local suave sobre las soluciones (para representar el avance de los jugadores en la partida)
* Partiremos de una población inicial aleatoria de jugadores

Por tanto, tendré que buscar unos valores para los parámetros que aseguren un comportamiento decente. Por ejemplo, creo que debo partir de una población con muchos individuos, pues a lo largo de la partida, irán quedando menos individuos en la partida.

# TODOs

* [ ] Elegir el número de jugadores en función a la dimensión con la que estemos trabajando
