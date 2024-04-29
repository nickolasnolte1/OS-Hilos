# Sistemas Operativos - UFM
# Proyecto de Hilos en Python

## Nickolas Nolte Carnet 20200561
## Esteban Samayoa Carnet 20200188


## Descripción

Este proyecto implementa un programa en Python para calcular estadísticas como la media, la desviación estándar, el mínimo, el máximo y el conteo de series de datos. El programa procesa 1000 archivos CSV en paralelo, utilizando diferentes configuraciones de hilos y núcleos de CPU para comparar el rendimiento.

## Objetivos

- Procesar archivos de datos en paralelo.
- Calcular estadísticas básicas para cada archivo.
- Analizar el impacto del paralelismo en el rendimiento del procesamiento.
- Ejecutar el programa en un entorno controlado usando Docker.

## Tecnologías Utilizadas

- Python 3.9
- Pandas: para el manejo de datos.
- Docker: para crear un entorno de ejecución reproducible.


## Configuración y Ejecución

### Pre-requisitos

- Docker instalado en tu máquina.
- Python 3.9 y Pandas instalados en el contenedor Docker.

### Construir la Imagen de Docker
Para construir la imagen de Docker, navega al directorio del proyecto y ejecuta:

```bash
docker build -t nombre_de_tu_imagen .
```

## Ejecutar el contenedor
Para ejecutar el programa dentro de Docker, utiliza el siguiente comando: `docker run --name nombre_del_contenedor -m 1g -v /ruta/en/host:/app/datos nombre_de_tu_imagen`

## Resultados
Los resultados de las estadísticas calculadas se guardan en archivos CSV dentro del directorio /resultados. Además, los tiempos de ejecución y el uso de recursos se monitorean para comparar el rendimiento entre diferentes configuraciones de paralelismo.
