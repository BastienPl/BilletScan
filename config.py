"""
Configuration de l'application BilletScan.
"""

import dash_bootstrap_components as dbc
import uuid
from pathlib import Path

# Constantes de l'application
APP_TITLE = 'BilletScan | Détecteur de faux billets'
EXTERNAL_STYLESHEETS = [
    dbc.themes.FLATLY, 
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css'
]

# Chemins des dossiers et fichiers
APP_FOLDER = Path(__file__).parent
MODEL_FOLDER = APP_FOLDER / 'models' / 'model_files'
MODEL_FILE = 'model_detection_billets.joblib'
MODEL_PATH = MODEL_FOLDER / MODEL_FILE


# Variable globale pour stocker la session
SESSION_ID = str(uuid.uuid4())

# Paramètres pour les visualisations
COLORS = {
    'authentic': '#28A745',   # Vert pour les billets authentiques
    'fake': '#DC3545',        # Rouge pour les billets contrefaits
    'primary': '#007BFF',     # Bleu primaire
}

# Caractéristiques des billets
BILL_FEATURES = ['diagonal', 'height_left', 'height_right', 'margin_low', 'margin_up', 'length']
FEATURE_LABELS = {
    "diagonal": "Diagonale",
    "height_left": "Hauteur gauche",
    "height_right": "Hauteur droite",
    "margin_low": "Marge basse",
    "margin_up": "Marge haute",
    "length": "Longueur",
    "is_fake": "Contrefait",
    "probability": "Niveau de confiance (%)",
}

def get_app_config():
    """Retourne la configuration pour l'initialisation de l'application."""
    return {
        'meta_tags': [
            {'name': 'viewport', 'content': 'width=device-width, initial-scale=1'},
            {'name': 'description', 'content': 'Application de détection de faux billets basée sur le machine learning'}
        ]
    }

# Autres paramètres globaux
def get_default_graph_layout():
    """Retourne la configuration de mise en page par défaut pour les graphiques."""
    return {
        "template": "plotly_white",
        "font": {"family": '"Segoe UI", Arial, sans-serif'}
    }