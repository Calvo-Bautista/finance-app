# Usar una imagen oficial de Python ligera
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Variables de entorno para evitar archivos .pyc y buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependencias del sistema si son necesarias (opcional)
# RUN apt-get update && apt-get install -y gcc

# Copiar requirements e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Exponer el puerto (Cloud Run usa la var PORT, por defecto 8080)
ENV PORT=8080

# Comando para ejecutar la aplicación usando uvicorn
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]