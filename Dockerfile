FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier uniquement les services nécessaires à la démo
COPY healthflow-api /app/healthflow-api
COPY healthflow-dashboard /app/healthflow-dashboard

# Fusion très simple des requirements
COPY healthflow-api/requirements.txt /app/req-api.txt
COPY healthflow-dashboard/requirements.txt /app/req-dashboard.txt
RUN pip install --no-cache-dir -r /app/req-api.txt && \
    pip install --no-cache-dir -r /app/req-dashboard.txt

# Script de démarrage qui lance API + Dashboard
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

EXPOSE 8501

CMD ["/app/start.sh"]
