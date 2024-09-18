# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos necesarios
COPY requirements.txt .
COPY app.py .
COPY sentiment_analysis.py .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Descargar recursos de NLTK
RUN python -c "import nltk; nltk.download('stopwords')"

# Exponer el puerto
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]