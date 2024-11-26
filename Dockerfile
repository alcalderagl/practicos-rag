# Usa una imagen base de Python
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos necesarios
COPY main_app.py /app/
COPY src /app/src/
COPY requirements.txt /app/

# Instala las dependencias
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Expone el puerto de la app de Streamlit
EXPOSE 8501

# Comando para ejecutar la app de Streamlit
CMD ["streamlit", "run", "main_app.py","--server.port=8501", "--server.enableCORS=false"]