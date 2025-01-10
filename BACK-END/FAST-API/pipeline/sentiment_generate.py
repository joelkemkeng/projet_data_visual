import pandas as pd
from textblob import TextBlob

def generate_sentiment_csv(
    input_csv: str,
    output_csv: str = "uber_data_with_sentiment.csv"
) -> pd.DataFrame:
    """
    Lit le CSV 'input_csv', génère une colonne 'sentiment' (positive ou negative),
    et enregistre le résultat dans 'output_csv'.
    
    Paramètres
    ----------
    input_csv : str
        Chemin vers le fichier CSV d'entrée.
    output_csv : str
        Chemin vers le fichier CSV de sortie (avec sentiment).
        
    Retour
    ------
    pd.DataFrame
        Le DataFrame résultant, contenant la nouvelle colonne 'sentiment'.
    """

    # 1) Lecture du CSV
    df = pd.read_csv(input_csv)
    
    # 2) Fonction pour calculer la polarité via TextBlob
    def get_polarity(text):
        if not isinstance(text, str):
            return 0.0  # On considère le texte vide comme neutre
        return TextBlob(text).sentiment.polarity
    
    # 3) Fonction pour classer la polarité en 2 classes : positive ou negative
    def classify_sentiment(polarity):
        # Seuil choisi : >= 0 = positive, < 0 = negative
        # Tu peux modifier ce seuil ou ajouter "neutral" si tu le souhaites
        return "positive" if polarity >= 0 else "negative"
    
    # 4) Calcul de la polarité pour chaque ligne de 'content'
    df['polarity'] = df['content'].apply(get_polarity)
    
    # 5) Classification du sentiment (positive/negative)
    df['sentiment'] = df['polarity'].apply(classify_sentiment)
    
    # 6) Sauvegarde du DataFrame résultant
    df.to_csv(output_csv, index=False)
    
    return df


if __name__ == "__main__":
    # Appel direct de la fonction pour tester
  
    df_sent = generate_sentiment_csv(
        input_csv="Assets/Datas/archive_uber/uber_data_cleaned.csv",
        output_csv="Assets/Datas/archive_uber/uber_data_sentiement.csv"
    )
    print("sentiment gener.")


