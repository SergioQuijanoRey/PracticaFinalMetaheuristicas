# Script que usamos para lanzar todos los experimentos
# Cuidado porque borra los resultados pasados que no hayan sido almacenados en otra carpeta

# Instalamos os paquetes necesarios
# Es necesario tener instalado pipenv
pipenv install

# Vamos al directorio indicado
cd ./src

# Generamos los archivos con cmake y make
cmake .
make

# Ejecutamos nuestras funciones
echo "Borramos los resultados pasados"
rm -rf results_battle_royale/
mkdir results_battle_royale
echo "Lanzamos los experimentos para Standar - dimension 10 "
pipenv run python3 main.py 10 standar
echo "Lanzamos los experimentos para Standar - dimension 30"
pipenv run python3 main.py 30 standar

# Movemos la carpeta a otra para que los resultados de memeticos no sobreescriban los resultados
mv results_battle_royale results_battle_royale_standar
mkdir results_battle_royale

# Lanzamos ahora la version memetica
echo "Lanzamos los experimentos para Memetic - dimension 10 "
pipenv run python3 main.py 10 memetic
echo "Lanzamos los experimentos para Memetic - dimension 30"
pipenv run python3 main.py 30 memetic

# Movemos la carpeta para que sea mas claro lo que representa
mv results_battle_royale results_battle_royale_memetic

# Volvemos al directorio original
cd -
