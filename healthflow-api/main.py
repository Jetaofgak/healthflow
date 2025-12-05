from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models, database, auth
import json

# Création tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="HealthFlow Score API")

# --- Initialisation : Créer un user de test au démarrage ---
@app.on_event("startup")
def create_test_user():
    db = database.SessionLocal()
    if not db.query(models.User).filter(models.User.username == "docteur").first():
        print("Création de l'utilisateur 'docteur'...")
        user = models.User(
            username="docteur",
            hashed_password=auth.get_password_hash("password123"),
            role="doctor"
        )
        db.add(user)
        db.commit()
    db.close()

# --- 1. Route de Login (pour obtenir le token) ---
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth.create_access_token(data={"sub": user.username, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

# --- 2. Route sécurisée : Voir le score d'un patient ---
@app.get("/api/v1/score/{pseudo_id}")
def get_patient_score(
    pseudo_id: str, 
    current_user: str = Depends(auth.get_current_user), # <--- Protection JWT ici
    db: Session = Depends(database.get_db)
):
    # On cherche la prédiction
    pred = db.query(models.RiskPrediction).filter(models.RiskPrediction.pseudo_id == pseudo_id).order_by(models.RiskPrediction.created_at.desc()).first()
    
    if not pred:
        raise HTTPException(status_code=404, detail="Aucun score disponible pour ce patient")

    return {
        "patient_id": pseudo_id,
        "risk_score": pred.risk_score,
        "risk_level": pred.risk_level,
        "analysis_date": pred.created_at,
        "details": json.loads(pred.shap_values_json),
        "consulted_by": current_user
    }
