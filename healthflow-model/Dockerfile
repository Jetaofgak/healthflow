# Image Python légère
FROM python:3.11-slim

# Pour éviter les problèmes de logs qui s'affichent pas
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Installation des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code
COPY . .

# La commande par défaut (sera surchargée par docker-compose, mais c'est bien d'en avoir une)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
