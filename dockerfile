# Usar una imagen base de Python oficial
FROM python:3.9-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos del proyecto al directorio de trabajo del contenedor
COPY . /app

# Instalar las dependencias del proyecto
RUN pip install pandas

# Comando para ejecutar el script Python cuando el contenedor se inicie
CMD ["python", "hilos.py"]
