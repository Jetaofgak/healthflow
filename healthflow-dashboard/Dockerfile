FROM python:3.11-slim

WORKDIR /app

# Installation des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code
COPY . .

# Streamlit a besoin de ces ports et variables spécifiques
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Commande de lancement
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
