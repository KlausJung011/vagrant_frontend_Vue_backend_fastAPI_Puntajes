#!/bin/bash

echo "..... iniciando configuraciones"

# 1. Actualizar paquetes
sudo apt-get update -y

# 2. Instalar Apache y Git
echo "..... instalando Apache y Git"
sudo apt-get install -y apache2 git

# 3. Limpiar la carpeta /var/www/html/ que tiene los archivos por defecto de Apache
echo "..... limpiando carpeta /var/www/html/"
sudo rm -rf /var/www/html/*

# 4. Clonar el repositorio del proyecto en la carpeta /var/www/html/
echo "..... clonando repositorio del proyecto"
REPO_URL="https://github.com/KlausJung011/PrograWeb1.git"
sudo git clone $REPO_URL /var/www/html/
# Sin barra al final para que se clone dentro de html y no cree una carpeta adicional
# sudo chown -R www-data:www-data /var/www/html
sudo chmod -R www-data:www-data /var/www/html

# 5. Verificar estado de Apache
echo "..... verificando estado de Apache"
sudo systemctl restart apache2

echo "--- configuración completada ---"