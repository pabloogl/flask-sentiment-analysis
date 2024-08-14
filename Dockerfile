# Usar una imagen base de Python
FROM python:3.9-alpine

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requisitos
COPY requirements.txt requirements.txt

# Instalar las dependencias
RUN pip install -r requirements.txt

# Copiar el resto del código de la aplicación
COPY . .

# Exponer el puerto 5000
EXPOSE 5000

# Definir el comando para ejecutar la aplicación
CMD ["python", "app.py"]