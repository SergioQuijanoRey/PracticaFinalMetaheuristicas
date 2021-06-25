# Práctica Final Metaheurísticas

* Repositorio para alojar el código de la práctica final, alternativa al examen de la asignatura
* Autor:
    * Sergio Quijano Rey
    * [Correo UGR](sergioquijano@correo.ugr.es)
* Metaheurística original basada en los juegos tipo *Battle Royale*
* Memoria donde se explica la inspiración y funcionamiento de la metaheurística: [PDF](https://github.com/SergioQuijanoRey/PracticaFinalMetaheuristicas/blob/master/Memoria/Memoria.pdf)
* A partir del código de [Daniel Molina](https://github.com/dmolina/cec2017real)

# Software necesario

* `python3`
* `pipenv`: el script `launch_experiments.sh` usa `pipenv` para instalar los paquetes necesarios
    * `numpy`

# Ejecución del Software

* Una vez instalado el software podemos ejecutar todos las funciones y sus repeticiones con el comando:

```bash
chmod u+x ./launch_experiments.sh && ./launch_experiments.sh
```
* Este comando lanza todo lo necesario para el estudio experimental que hacemos en la memoria de las prácticas
    1. Instala los paquetes necesarios usando `pipenv`
    2. Crea las carpetas necesarias para almacenar los resultados del algoritmo
    3. Hace `cmake` y `make` para el código `C`
    4. Borra los resultados pasados y crea las carpetas necesarias
    5. Lanza todas las búsquedas y organiza los resultados
