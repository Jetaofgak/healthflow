import streamlit as st
import requests
import pandas as pd
import json

# Config
API_URL = "http://localhost:8085" # L'API sécurisée
TOKEN = None

st.set_page_config(page_title="HealthFlow AI Dashboard", layout="wide")

# --- Sidebar : Connexion ---
st.sidebar.title("🔐 Connexion Médecin")
username = st.sidebar.text_input("Username", "docteur")
password = st.sidebar.text_input("Password", type="password")

if st.sidebar.button("Se connecter"):
    try:
        resp = requests.post(f"{API_URL}/token", data={"username": username, "password": password})
        if resp.status_code == 200:
            st.session_state['token'] = resp.json()['access_token']
            st.sidebar.success("Connecté !")
        else:
            st.sidebar.error("Erreur auth")
    except:
        st.sidebar.error("API hors ligne")

# --- Main Page ---
st.title("🏥 HealthFlow: Prédiction de Réadmission")

if 'token' in st.session_state:
    # Zone de recherche
    patient_id = st.text_input("Rechercher un Patient ID (Pseudo-ID)", "6fe631e8ce4e")
    
    if st.button("Analyser"):
        headers = {"Authorization": f"Bearer {st.session_state['token']}"}
        resp = requests.get(f"{API_URL}/api/v1/score/{patient_id}", headers=headers)
        
        if resp.status_code == 200:
            data = resp.json()
            
            # Colonnes pour l'affichage
            col1, col2, col3 = st.columns(3)
            col1.metric("Niveau de Risque", data['risk_level'])
            col2.metric("Score Probabilité", f"{data['risk_score']:.2%}")
            col3.info(f"Analysé par : {data['consulted_by']}")
            
            # Graphique SHAP (Explications)
            st.subheader("🔍 Explication de l'IA (SHAP Values)")
            shap_data = data['details']
            df_shap = pd.DataFrame(list(shap_data.items()), columns=['Facteur', 'Impact'])
            st.bar_chart(df_shap.set_index('Facteur'))
            
        else:
            st.error("Patient introuvable ou erreur serveur.")
else:
    st.warning("Veuillez vous connecter dans le menu latéral.")
