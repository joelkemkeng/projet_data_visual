notebook Jupyter dans un environnement Python spécifique :

    Installer ipykernel dans l’environnement
    Sélectionner l’environnement dans la barre de sélection du kernel (en haut à droite dans le notebook)

1. Installer ipykernel dans l’environnement

Même si tu as déjà installé pandas, numpy, etc., il faut également que l’environnement dispose du package ipykernel.
Depuis un Terminal (ou dans VS Code, un terminal intégré) activé sur ton environnement virtuel, tape :

pip install ipykernel

Ensuite, tu peux ajouter le kernel de cet environnement :

python -m ipykernel install --user --name nom_de_ton_env --display-name "MonEnv"

    nom_de_ton_env : doit être un identifiant unique (pas d’espace).
    "MonEnv" : c’est juste le nom lisible qui apparaîtra dans la liste des kernels de Jupyter.

2. Sélectionner l’environnement dans VS Code

Dans un notebook .ipynb sous VS Code :

    En haut à droite, tu as un menu déroulant qui indique le kernel actuellement utilisé (par exemple, Python 3.10, Python 3.11, Global Env, etc.).
    Clique dessus, et tu verras apparaître la liste des environnements disponibles.
    Choisis celui que tu as installé avec ipykernel et que tu viens de créer (par exemple, "MonEnv").

Une fois le kernel sélectionné, relance le notebook, et tu devrais voir que le Python utilisé dans le notebook correspond à ton environnement virtuel (avec toutes tes librairies installées).



Charger dataset → 2. Fusion colonnes → 3. Drop colonnes inutiles → 4. Conversions → 5. Drop lignes vides → 6. Export