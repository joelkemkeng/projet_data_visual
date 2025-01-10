# main.py

from fastapi import FastAPI, HTTPException
import pandas as pd

from fastapi.middleware.cors import CORSMiddleware




from kpi_function.kpi import (
    get_total_reviews,
    get_score_distribution,
    get_sentiment_ratio,
    get_average_score_over_time,
    get_reviews_by_version,
    get_thumbs_up_distribution,
    get_combined_sentiment_average,
    get_most_common_words,
    get_average_thumbs_up_per_sentiment,
    get_review_frequency_by_hour,
    get_top_users_by_reviews,
    get_score_thumbs_correlation,
    get_reviews_per_user,
    get_average_score_per_user,
    get_sentiment_trends_by_version,
    get_monthly_review_count
)
from typing import List, Optional

app = FastAPI()



# Configuration CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    # Ajoutez d'autres origines si nécessaire
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
   
)

# Charger le DataFrame nettoyé et enrichi au démarrage de l'API
try:
    df = pd.read_csv("Assets/Datas/archive_uber/uber_data_final.csv")
    df['at'] = pd.to_datetime(df['at'])
except FileNotFoundError:
    raise HTTPException(status_code=404, detail="Fichier uber_data_final.csv non trouvé dans le dossier data/")

@app.get("/")
def read_root():
    """
    Endpoint racine pour vérifier que l'API fonctionne.
    """
    return {"message": "Bienvenue sur l'API des KPI Uber!"}

@app.get("/total_reviews")
def total_reviews():
    """
    Endpoint pour obtenir le nombre total d'avis.
    """
    total = get_total_reviews(df)
    return {"total_reviews": total}

@app.get("/score_distribution")
def score_distribution():
    """
    Endpoint pour obtenir la distribution des scores.
    """
    distribution_df = get_score_distribution(df)
    return distribution_df.to_dict(orient="records")

@app.get("/sentiment_ratio")
def sentiment_ratio():
    """
    Endpoint pour obtenir la proportion des sentiments.
    """
    ratio = get_sentiment_ratio(df)
    return ratio

@app.get("/average_score_over_time")
def average_score_over_time(freq: Optional[str] = 'M'):
    """
    Endpoint pour obtenir la note moyenne des avis par période.
    Paramètre 'freq' : fréquence de regroupement (e.g., 'D', 'W', 'M').
    """
    avg_score_df = get_average_score_over_time(df, freq)
    return avg_score_df.to_dict(orient="records")

@app.get("/reviews_by_version")
def reviews_by_version():
    """
    Endpoint pour obtenir le nombre d'avis et la note moyenne par version de l'application.
    """
    reviews_version_df = get_reviews_by_version(df)
    return reviews_version_df.to_dict(orient="records")

@app.get("/thumbs_up_distribution")
def thumbs_up_distribution():
    """
    Endpoint pour obtenir la distribution des 'thumbsUpCount'.
    """
    thumbs_up_df = get_thumbs_up_distribution(df)
    return thumbs_up_df.to_dict(orient="records")

@app.get("/combined_sentiment_average")
def combined_sentiment_average():
    """
    Endpoint pour obtenir la moyenne des scores combinés.
    """
    avg_combined = get_combined_sentiment_average(df)
    return {"average_combined_score": round(avg_combined, 2)}

@app.get("/most_common_words")
def most_common_words(sentiment: str, top_n: Optional[int] = 10):
    """
    Endpoint pour obtenir les mots les plus fréquents dans les avis d'un certain sentiment.
    Paramètres :
        - sentiment : 'positive', 'negative', ou 'neutral'
        - top_n : nombre de mots à retourner (par défaut 10)
    """
    if sentiment not in ['positive', 'negative', 'neutral']:
        raise HTTPException(status_code=400, detail="Le sentiment doit être 'positive', 'negative' ou 'neutral'.")
    
    common_words = get_most_common_words(df, sentiment, top_n)
    return {"common_words": common_words}

@app.get("/average_thumbs_up_per_sentiment")
def average_thumbs_up_per_sentiment():
    """
    Endpoint pour obtenir la moyenne des 'thumbsUpCount' par catégorie de sentiment.
    """
    avg_thumbs_df = get_average_thumbs_up_per_sentiment(df)
    return avg_thumbs_df.to_dict(orient="records")

@app.get("/review_frequency_by_hour")
def review_frequency_by_hour():
    """
    Endpoint pour obtenir la fréquence des avis par heure de la journée.
    """
    frequency_df = get_review_frequency_by_hour(df)
    return frequency_df.to_dict(orient="records")

@app.get("/top_users_by_reviews")
def top_users_by_reviews(top_n: Optional[int] = 10):
    """
    Endpoint pour obtenir les utilisateurs ayant laissé le plus grand nombre d'avis.
    Paramètre 'top_n' : nombre d'utilisateurs à retourner (par défaut 10)
    """
    top_users_df = get_top_users_by_reviews(df, top_n)
    return top_users_df.to_dict(orient="records")

@app.get("/score_thumbs_correlation")
def score_thumbs_correlation():
    """
    Endpoint pour obtenir le coefficient de corrélation entre 'score' et 'thumbsUpCount'.
    """
    correlation = get_score_thumbs_correlation(df)
    return {"score_thumbs_correlation": round(correlation, 2)}

@app.get("/reviews_per_user")
def reviews_per_user():
    """
    Endpoint pour obtenir le nombre d'avis laissés par chaque utilisateur.
    """
    reviews_user_df = get_reviews_per_user(df)
    return reviews_user_df.to_dict(orient="records")

@app.get("/average_score_per_user")
def average_score_per_user():
    """
    Endpoint pour obtenir la note moyenne attribuée par chaque utilisateur.
    """
    avg_score_user_df = get_average_score_per_user(df)
    return avg_score_user_df.to_dict(orient="records")

@app.get("/sentiment_trends_by_version")
def sentiment_trends_by_version(freq: Optional[str] = 'M'):
    """
    Endpoint pour obtenir les tendances de sentiment par version de l'application.
    Paramètre 'freq' : fréquence de regroupement temporel (e.g., 'D', 'W', 'M').
    """
    sentiment_trends_df = get_sentiment_trends_by_version(df, freq)
    # Convertir les dates en format string pour une meilleure compatibilité JSON
    sentiment_trends_df['at'] = sentiment_trends_df['at'].dt.strftime('%Y-%m-%d')
    return sentiment_trends_df.to_dict(orient="records")




@app.get("/monthly_reviews")
def monthly_reviews():
    """
    Endpoint pour obtenir le nombre d'avis pour chaque mois.
    """
    monthly_reviews_df = get_monthly_review_count(df)
    
    
    # Préparer les données pour ECharts
    data = {
        "months": monthly_reviews_df["month"].tolist(),
        "review_counts": monthly_reviews_df["review_count"].tolist()
    }
    
    
    return data
