"""
Chargement et gestion du modèle de machine learning.
"""

import joblib
from config import MODEL_PATH

def load_model():
    """
    Charge le modèle à partir du fichier.
    
    Returns:
        Le modèle chargé ou None si le modèle n'est pas trouvé.
    """
    try:
        if not MODEL_PATH.is_file():
            print(f"Fichier de modèle non trouvé: {MODEL_PATH}")
            return None
            
        model = joblib.load(MODEL_PATH)
        print(f"Modèle chargé avec succès: {MODEL_PATH.name}")
        return model
    except Exception as e:
        print(f"Erreur lors du chargement du modèle: {str(e)}")
        return None

# Chargement du modèle au démarrage
clf = load_model()

def predict(X):
    """
    Effectue une prédiction avec le modèle chargé.
    
    Args:
        X (pandas.DataFrame): Les caractéristiques d'entrée.
        
    Returns:
        tuple: Un tuple contenant (y_pred, y_proba) ou (None, None) si le modèle n'est pas chargé.
    """
    if clf is None:
        return None, None
        
    try:
        y_pred = clf.predict(X)
        y_proba = clf.predict_proba(X)
        return y_pred, y_proba
    except Exception as e:
        print(f"Erreur lors de la prédiction: {str(e)}")
        return None, None

