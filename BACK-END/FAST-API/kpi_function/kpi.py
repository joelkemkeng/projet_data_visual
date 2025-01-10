# kpi_functions.py

import pandas as pd
from collections import Counter
import re

def get_total_reviews(df: pd.DataFrame) -> int:
    """
    Retourne le nombre total d'avis dans le DataFrame.

    Paramètres
    ----------
    df : pd.DataFrame
        DataFrame contenant les avis utilisateurs.

    Retour
    ------
    int
        Nombre total d'avis.
    """
    total = df.shape[0]
    return total

def get_score_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """
    Retourne la distribution des scores (1 à 5).

    Paramètres
    ----------
    df : pd.DataFrame
        DataFrame contenant les avis utilisateurs.

    Retour
    ------
    pd.DataFrame
        DataFrame avec deux colonnes : 'score' et 'count'.
    """
    distribution = df['score'].value_counts().sort_index().reset_index()
    distribution.columns = ['score', 'count']
    return distribution

def get_sentiment_ratio(df: pd.DataFrame) -> dict:
    """
    Calcule la proportion des sentiments 'positive', 'negative', et 'neutral'.

    Paramètres
    ----------
    df : pd.DataFrame
        DataFrame contenant les avis utilisateurs.

    Retour
    ------
    dict
        Dictionnaire avec les proportions des sentiments en pourcentage.
    """
    total = df.shape[0]
    sentiment_counts = df['sentiment'].value_counts().to_dict()
    sentiment_ratio = {k: round(v / total * 100, 2) for k, v in sentiment_counts.items()}
    return sentiment_ratio

def get_average_score_over_time(df: pd.DataFrame, freq: str = 'ME') -> pd.DataFrame:
    """
    Calcule la note moyenne des avis par période (par défaut, par mois).

    Paramètres
    ----------
    df : pd.DataFrame
        DataFrame contenant les avis utilisateurs.
    freq : str
        Fréquence de regroupement (e.g., 'D' pour jour, 'W' pour semaine, 'M' pour mois).

    Retour
    ------
    pd.DataFrame
        DataFrame avec la date et la note moyenne correspondante.
    """
    # S'assurer que la colonne 'at' est de type datetime
    df['at'] = pd.to_datetime(df['at'])
    
    # Grouper par la fréquence choisie et calculer la moyenne des scores
    average_score = df.resample(freq, on='at')['score'].mean().reset_index()
    average_score.rename(columns={'score': 'average_score'}, inplace=True)
    
    return average_score

def get_reviews_by_version(df: pd.DataFrame) -> pd.DataFrame:
    """
    Retourne le nombre d'avis et la note moyenne par version de l'application.

    Paramètres
    ----------
    df : pd.DataFrame
        DataFrame contenant les avis utilisateurs.

    Retour
    ------
    pd.DataFrame
        DataFrame avec 'reviewCreatedVersion', 'review_count', et 'average_score'.
    """
    grouped = df.groupby('reviewCreatedVersion').agg(
        review_count=pd.NamedAgg(column='content', aggfunc='count'),
        average_score=pd.NamedAgg(column='score', aggfunc='mean')
    ).reset_index()
    return grouped

def get_thumbs_up_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyse la distribution des 'thumbsUpCount'.

    Paramètres
    ----------
    df : pd.DataFrame
        DataFrame contenant les avis utilisateurs.

    Retour
    ------
    pd.DataFrame
        DataFrame avec la distribution des 'thumbsUpCount'.
    """
    distribution = df['thumbsUpCount'].value_counts().sort_index().reset_index()
    distribution.columns = ['thumbsUpCount', 'count']
    return distribution

def get_combined_sentiment_average(df: pd.DataFrame) -> float:
    """
    Calcule la moyenne des scores combinés.

    Paramètres
    ----------
    df : pd.DataFrame
        DataFrame contenant les avis utilisateurs.

    Retour
    ------
    float
        Moyenne des 'combined_score'.
    """
    return df['combined_score'].mean()

def get_most_common_words(df: pd.DataFrame, sentiment: str, top_n: int = 10) -> list:
    """
    Retourne les mots les plus fréquents dans les avis d'un certain sentiment.

    Paramètres
    ----------
    df : pd.DataFrame
        DataFrame contenant les avis utilisateurs.
    sentiment : str
        Sentiment à filtrer ('positive', 'negative', 'neutral').
    top_n : int
        Nombre de mots à retourner.

    Retour
    ------
    list
        Liste des mots les plus fréquents sous forme de tuples (mot, fréquence).
    """
    # Filtrer les avis selon le sentiment
    filtered_df = df[df['sentiment'] == sentiment]
    
    # Concaténer tous les textes des avis filtrés
    all_text = ' '.join(filtered_df['content'].astype(str))
    
    # Nettoyer le texte : enlever les caractères spéciaux et mettre en minuscules
    all_text = re.sub(r'[^a-zA-Z\s]', '', all_text).lower()
    
    # Séparer en mots
    words = all_text.split()
    
    # Compter les mots
    word_counts = Counter(words)
    
    # Retourner les top_n mots
    return word_counts.most_common(top_n)

def get_average_thumbs_up_per_sentiment(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcule la moyenne des 'thumbsUpCount' pour chaque catégorie de sentiment.

    Paramètres
    ----------
    df : pd.DataFrame
        DataFrame contenant les avis utilisateurs.

    Retour
    ------
    pd.DataFrame
        DataFrame avec 'sentiment' et 'average_thumbs_up'.
    """
    average_thumbs = df.groupby('sentiment')['thumbsUpCount'].mean().reset_index()
    average_thumbs.rename(columns={'thumbsUpCount': 'average_thumbs_up'}, inplace=True)
    return average_thumbs

def get_review_frequency_by_hour(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcule le nombre d'avis soumis à chaque heure de la journée.

    Paramètres
    ----------
    df : pd.DataFrame
        DataFrame contenant les avis utilisateurs.

    Retour
    ------
    pd.DataFrame
        DataFrame avec 'hour' et 'review_count'.
    """
    # Extraire l'heure de la colonne 'at'
    df['hour'] = pd.to_datetime(df['at']).dt.hour
    
    # Compter le nombre d'avis par heure
    frequency = df['hour'].value_counts().sort_index().reset_index()
    frequency.columns = ['hour', 'review_count']
    
    return frequency

def get_top_users_by_reviews(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Identifie les utilisateurs ayant laissé le plus grand nombre d'avis.

    Paramètres
    ----------
    df : pd.DataFrame
        DataFrame contenant les avis utilisateurs.
    top_n : int
        Nombre d'utilisateurs à retourner.

    Retour
    ------
    pd.DataFrame
        DataFrame avec 'userName' et 'review_count'.
    """
    top_users = df['userName'].value_counts().head(top_n).reset_index()
    top_users.columns = ['userName', 'review_count']
    return top_users

def get_score_thumbs_correlation(df: pd.DataFrame) -> float:
    """
    Calcule le coefficient de corrélation entre 'score' et 'thumbsUpCount'.

    Paramètres
    ----------
    df : pd.DataFrame
        DataFrame contenant les avis utilisateurs.

    Retour
    ------
    float
        Coefficient de corrélation entre 'score' et 'thumbsUpCount'.
    """
    # Calculer la corrélation en excluant les valeurs manquantes
    correlation = df[['score', 'thumbsUpCount']].corr().iloc[0,1]
    return correlation

def get_reviews_per_user(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcule le nombre d'avis laissés par chaque utilisateur.

    Paramètres
    ----------
    df : pd.DataFrame
        DataFrame contenant les avis utilisateurs.

    Retour
    ------
    pd.DataFrame
        DataFrame avec 'userName' et 'review_count'.
    """
    reviews_per_user = df['userName'].value_counts().reset_index()
    reviews_per_user.columns = ['userName', 'review_count']
    return reviews_per_user

def get_average_score_per_user(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcule la note moyenne attribuée par chaque utilisateur.

    Paramètres
    ----------
    df : pd.DataFrame
        DataFrame contenant les avis utilisateurs.

    Retour
    ------
    pd.DataFrame
        DataFrame avec 'userName' et 'average_score'.
    """
    average_score = df.groupby('userName')['score'].mean().reset_index()
    average_score.rename(columns={'score': 'average_score'}, inplace=True)
    return average_score

def get_sentiment_trends_by_version(df: pd.DataFrame, freq: str = 'M') -> pd.DataFrame:
    """
    Suivi des tendances de sentiment pour chaque version de l'application.

    Paramètres
    ----------
    df : pd.DataFrame
        DataFrame contenant les avis utilisateurs.
    freq : str
        Fréquence de regroupement temporel (ex. 'M' pour mois).

    Retour
    ------
    pd.DataFrame
        DataFrame avec 'reviewCreatedVersion', 'at', 'sentiment', et 'count'.
    """
    # S'assurer que la colonne 'at' est de type datetime
    df['at'] = pd.to_datetime(df['at'])
    
    # Grouper par version, période, et sentiment, puis compter les occurrences
    grouped = df.groupby(['reviewCreatedVersion', pd.Grouper(key='at', freq=freq), 'sentiment']).size().reset_index(name='count')
    
    return grouped







def get_monthly_review_count(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcule le nombre d'avis pour chaque mois.

    Paramètres
    ----------
    df : pd.DataFrame
        DataFrame contenant les avis utilisateurs.

    Retour
    ------
    pd.DataFrame
        DataFrame avec deux colonnes : 'month' et 'review_count'.
    """
    # Convertir la colonne 'at' en datetime si ce n'est pas déjà fait
    df['at'] = pd.to_datetime(df['at'])

    # Grouper par mois et compter les avis
    monthly_reviews = df.resample('M', on='at').size().reset_index(name='review_count')
    monthly_reviews['month'] = monthly_reviews['at'].dt.strftime('%Y-%m')
    monthly_reviews = monthly_reviews[['month', 'review_count']]
    
    return monthly_reviews
