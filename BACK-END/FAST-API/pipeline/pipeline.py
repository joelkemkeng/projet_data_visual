import pandas as pd
from sentiment_note_gen import generate_sentiment_with_score_csv


def clean_uber_data_notebook_style(
    input_csv: str = "../Assets/Datas/archive_uber/uber_data.csv",
    output_csv: str = "../Assets/Datas/archive_uber/uber_data_cleaned.csv"
) -> pd.DataFrame:
    """
    les étapes de nettoyage Uber Reviews.
    
    1. Lecture du fichier CSV d'entrée
    2. Drop des colonnes inutiles ('userImage')
    3. Fusion de 'reviewCreatedVersion' et 'appVersion'
    4. Suppression de 'appVersion' (devenue redondante)
    5. Conversion de 'at' en datetime
    6. Conversion de 'repliedAt' en datetime (si besoin)
    7. Gérer les manquants dans 'replyContent' (remplir par 'No reply')
    8. Vérification du type pour 'score' et 'thumbsUpCount'
    9. (Optionnel) Création de la colonne 'response_time_hours'
    10. Supprimer les colonnes 'replyContent' et 'repliedAt' (finalement jugées inutiles)
    11. Supprimer les lignes qui restent vides (df.dropna)
    12. Sauvegarder le résultat dans un CSV final
    """

    # 1. Lecture du CSV
    df = pd.read_csv(input_csv)
    
    # 2. Drop des colonnes inutiles
    #    (Comme dans le notebook : "df.drop(columns=['userImage'], inplace=True)  # On n'en a pas besoin")
    if 'userImage' in df.columns:
        df.drop(columns=['userImage'], inplace=True)  # On n'en a pas besoin

    # 3. Gérer les versions : si 'reviewCreatedVersion' est vide, on met 'appVersion'
    df['reviewCreatedVersion'] = df['reviewCreatedVersion'].fillna(df['appVersion'])

    # 4. Choisir de supprimer 'appVersion' après ce merge si elles sont redondantes
    if 'appVersion' in df.columns:
        df.drop(columns=['appVersion'], inplace=True)

    # 5. Convertir la colonne 'at' en datetime
    df['at'] = pd.to_datetime(df['at'], errors='coerce')

    # 6. Convertir la colonne 'repliedAt' en datetime (si besoin)
    if 'repliedAt' in df.columns:
        df['repliedAt'] = pd.to_datetime(df['repliedAt'], errors='coerce')

    # 7. Gérer les manquants dans 'replyContent'
    #    (remplir par 'No reply')
    if 'replyContent' in df.columns:
        df['replyContent'] = df['replyContent'].fillna('No reply')

    # 8. Vérification du type sur 'score' et 'thumbsUpCount'
    #    (conversion en int, en remplissant éventuellement par 0)
    if 'score' in df.columns:
        df['score'] = df['score'].astype(int)
    if 'thumbsUpCount' in df.columns:
        df['thumbsUpCount'] = df['thumbsUpCount'].fillna(0).astype(int)

    # (Comme dans le notebook, un petit df.info() et df.head() pouvaient suivre ici,
    #  mais on les commente ou on les supprime dans la fonction.)

    # ------
    # INSTRUCTIONS FINALES
    # "IL FAUT SUPPRIMER userImage, replyContent, repliedAt CAR ILS SONT VIDES"
    # -> userImage est déjà supprimée en étape 2
    # -> on supprime replyContent et repliedAt maintenant
    # ------
    cols_to_drop_final = []
    if 'replyContent' in df.columns:
        cols_to_drop_final.append('replyContent')
    if 'repliedAt' in df.columns:
        cols_to_drop_final.append('repliedAt')
    
    if cols_to_drop_final:
        df.drop(columns=cols_to_drop_final, inplace=True)

    # "apres avoir supprimer un, supprimer les ligne qui ont les cases vides"
    df.dropna(inplace=True)

    # 12. Sauvegarde du DataFrame final
    df.to_csv(output_csv, index=False)
    
    #  message pour confirmer que tout s'est bien passé
    print("Fichier de sortie généré traitemnt data de base :", output_csv)
    
    
    input_file = "Assets/Datas/archive_uber/uber_data_cleaned.csv"
    output_file = "Assets/Datas/archive_uber/uber_data_final.csv"

    # Appel de la fonction, avec un alpha à 70%
    df_result = generate_sentiment_with_score_csv(
        input_csv=input_file,
        output_csv=output_file,
        alpha=0.7
    )
    
    #  message pour confirmer que tout s'est bien passé
    print("Fichier de sortie généré avec les sentiement traiter :", output_file)
    print("Aperçu du DataFrame :")
    print(df_result.head(5))

    
    
    
    return df



if __name__ == "__main__":
    # Appel direct de la fonction pour tester
    
    clean_uber_data_notebook_style(
        input_csv="Assets/Datas/archive_uber/uber_data.csv",
        output_csv="Assets/Datas/archive_uber/uber_data_cleaned.csv"
    )
    print("Traitement effectué.")