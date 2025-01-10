import pandas as pd
from textblob import TextBlob
import emoji

def generate_sentiment_with_score_csv(
    input_csv: str,
    output_csv: str = "uber_data_with_combined_sentiment.csv",
    alpha: float = 0.7
) -> pd.DataFrame:
    """
    Cette fonction lit un fichier CSV qui doit contenir au moins les colonnes 'content' (le texte de l'avis)
    et 'score' (la note 1 à 5). Elle calcule un score de sentiment combiné en prenant en compte
    à la fois la polarité du texte (via TextBlob) et la note numérique de l'utilisateur.

    Le résultat est ensuite enregistré dans un nouveau CSV (output_csv).
    On ajoute :
      - 'combined_score' : la valeur numérique résultante de la combinaison.
      - 'sentiment' : le label final ("positive", "negative" ou "neutral"),
                      déterminé par la fonction classify_combined.

    Paramètres:
    -----------
    input_csv : str
        Chemin complet (ou relatif) vers le fichier CSV d'entrée (doit avoir 'content' et 'score').
    output_csv : str
        Nom (ou chemin) du fichier CSV de sortie, où l'on va sauver les données avec la colonne 'sentiment'.
    alpha : float
        Coefficient de pondération de la polarité du texte.
        (1 - alpha) sera la pondération attribuée à la note utilisateur (score).

    Retourne:
    ---------
    pd.DataFrame
        Le DataFrame final, contenant notamment les colonnes 'combined_score' et 'sentiment'.
    
    Remarques:
    ----------
    - On utilise la librairie 'emoji' pour "demojiser" le texte et permettre à TextBlob
      de mieux interpréter certains smileys.
    - TextBlob est plus efficace pour du texte en anglais. Si les avis sont dans d'autres langues,
      il peut y avoir des imprécisions.
    - Le paramètre alpha peut être ajusté si on veut donner plus ou moins d'importance
      à la polarité textuelle vs. la note 1-5 donnée par l'utilisateur.
    """

    # ------------------------------------------------------------------------
    # Contrôle d'existence des colonnes dans le CSV
    # ------------------------------------------------------------------------
    df = pd.read_csv(input_csv)
    if 'content' not in df.columns or 'score' not in df.columns:
        raise ValueError(
            "Le fichier CSV doit contenir les colonnes 'content' et 'score'."
        )
    
    # ------------------------------------------------------------------------
    # Sous-fonction get_text_polarity: calcule la polarité du texte
    # ------------------------------------------------------------------------
    def get_text_polarity(text: str) -> float:
        """
        Calcule la polarité d'un texte via TextBlob.
        -1.0 = très négatif
         0.0 = neutre
         1.0 = très positif

        On "demojise" le texte pour transformer les émojis en code du style :smiley:
        afin que TextBlob puisse éventuellement déceler une intention.
        """
        if not isinstance(text, str):
            # Si le contenu n'est pas une chaîne, on renvoie 0.0 par défaut (neutre)
            return 0.0
        
        # Transforme les éventuels émojis en code textuel
        text_no_emoji = emoji.demojize(text)
        
        # Détermine la polarité via TextBlob
        return TextBlob(text_no_emoji).sentiment.polarity

    # ------------------------------------------------------------------------
    # Sous-fonction scale_score: transforme un score 1..5 en une échelle -1..+1
    # ------------------------------------------------------------------------
    def scale_score(score_value: float) -> float:
        """
        Convertit la note sur 5 en un intervalle [-1, +1].
        Exemple:
          - score=1 => -1.0
          - score=3 =>  0.0
          - score=5 => +1.0

        Formule utilisée: (score - 3) / 2
        """
        return (score_value - 3) / 2

    # ------------------------------------------------------------------------
    # Sous-fonction combined_sentiment: combine polarité texte et note
    # ------------------------------------------------------------------------
    def combined_sentiment(text: str, score_value: float) -> float:
        """
        Calcule un score numérique qui prend en compte à la fois:
        - La polarité textuelle (entre -1 et +1, calculée par TextBlob).
        - La note de l'utilisateur (entre 1 et 5, qu'on convertit en [-1..+1]).

        On fait une moyenne pondérée:
          combined = alpha * polarité_texte + (1 - alpha) * polarité_score

        alpha est le poids qu'on donne à la polarité du texte.
        (1 - alpha) est donc le poids accordé à la note.

        Retourne un float, qui peut être positif ou négatif.
        """
        pol_text = get_text_polarity(text)
        pol_score = scale_score(score_value)
        return alpha * pol_text + (1 - alpha) * pol_score

    # ------------------------------------------------------------------------
    # Sous-fonction classify_combined: on utilise trois labels
    # ------------------------------------------------------------------------
    def classify_combined(value: float) -> str:
        """
        Cette fonction prend un score numérique (value),
        et détermine s'il doit être considéré comme 'positive', 'negative'
        ou 'neutral', selon les seuils choisis.

        On a fixé deux seuils simples :
        - Si value est supérieur à 0.1, on renvoie 'positive'.
        - Si value est inférieur à -0.1, on renvoie 'negative'.
        - Sinon, on considère que c'est 'neutral'.

        Pourquoi ces valeurs de 0.1 et -0.1 ?
        -------------------------------------
        On laisse une petite "zone tampon" entre -0.1 et +0.1
        pour capturer tout ce qui est jugé ni franchement positif,
        ni franchement négatif. On peut ainsi éviter de dire
        qu'un avis est "positif" ou "négatif" quand la valeur
        est très proche de zéro.

        Ces seuils restent arbitraires et peuvent être ajustés
        en fonction des besoins et de la sensibilité souhaitée.
        Par exemple, on pourrait choisir 0.05 ou 0.2 comme limites.
        L'essentiel est de trouver un compromis cohérent avec
        la façon dont on veut catégoriser les retours utilisateurs.
        """
        if value > 0.1:
            return "positive"
        elif value < -0.1:
            return "negative"
        else:
            return "neutral"

    # ------------------------------------------------------------------------
    # Application de combined_sentiment à chaque ligne du DataFrame
    # ------------------------------------------------------------------------
    # On crée une nouvelle colonne 'combined_score' pour garder la valeur numérique
    df['combined_score'] = df.apply(
        lambda row: combined_sentiment(row['content'], row['score']),
        axis=1
    )

    # On crée la colonne 'sentiment' pour catégoriser le résultat final
    df['sentiment'] = df['combined_score'].apply(classify_combined)

    # ------------------------------------------------------------------------
    # Sauvegarde du DataFrame (avec ses nouvelles colonnes) dans le CSV de sortie
    # ------------------------------------------------------------------------
    df.to_csv(output_csv, index=False)

    # On retourne également le DataFrame pour usage direct (ex: affichage, analyse)
    return df


if __name__ == "__main__":
    # Exemple d'appel direct pour tester le script
    # On peut exécuter ce fichier .py directement et vérifier le fichier de sortie
    df_result = generate_sentiment_with_score_csv(
        input_csv="Assets/Datas/archive_uber/uber_data_cleaned.csv",
        output_csv="Assets/Datas/archive_uber/uber_data_with_combined_sentiment.csv",
        alpha=0.7  # 70% de poids pour le texte, 30% pour la note (score utilisateur)
    )
    print("Le sentiment combiné a été calculé et le fichier de sortie est généré.")
    print(df_result.head(5))  # Affichage d'un aperçu des 5 premières lignes.
