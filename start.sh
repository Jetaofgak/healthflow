#!/bin/sh
# Lancer l'API sur le port 8085
cd /app/healthflow-api
uvicorn main:app --host 0.0.0.0 --port 8085 &

# Lancer le dashboard Streamlit sur le port 8501
cd /app/healthflow-dashboard
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
