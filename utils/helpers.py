"""
Fonctions utilitaires pour l'application BilletScan.
"""

import base64
import io
import pandas as pd
import numpy as np
from config import SESSION_ID

# Variables globales pour stocker les données entre les callbacks
df = None
df_results = None

def parse_csv_contents(contents, filename):
    """
    Parse le contenu d'un fichier CSV téléchargé.
    
    Args:
        contents (str): Contenu du fichier encodé en base64.
        filename (str): Nom du fichier.
        
    Returns:
        tuple: (DataFrame, message d'erreur) où le DataFrame est None en cas d'erreur.
    """
    if contents is None:
        return None, "Aucun fichier sélectionné."
    
    try:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        return df, None
    except Exception as e:
        return None, f"Erreur lors de la lecture du fichier: {str(e)}"

def validate_dataframe(df, required_columns):
    """
    Valide un DataFrame pour s'assurer qu'il contient les colonnes requises et pas de valeurs manquantes.
    
    Args:
        df (pandas.DataFrame): Le DataFrame à valider.
        required_columns (list): Liste des colonnes requises.
        
    Returns:
        tuple: (bool, message d'erreur) où le booléen indique si le DataFrame est valide.
    """
    if df is None:
        return False, "Données non disponibles."
    
    # Vérification des colonnes requises
    df_columns = set(df.columns)
    missing_columns = set(required_columns) - df_columns
    
    if missing_columns:
        return False, f"Colonnes manquantes: {', '.join(missing_columns)}"
    
    # Vérification des valeurs manquantes
    if df.isna().any().any():
        missing_in_cols = df.columns[df.isna().any()].tolist()
        return False, f"Valeurs manquantes dans: {', '.join(missing_in_cols)}"
    
    return True, None

def create_results_dataframe(ids, y_pred, y_proba):
    """
    Crée un DataFrame de résultats à partir des prédictions du modèle.
    
    Args:
        ids (list): Identifiants des billets.
        y_pred (numpy.ndarray): Prédictions du modèle (0 ou 1).
        y_proba (numpy.ndarray): Probabilités prédites par le modèle.
        
    Returns:
        pandas.DataFrame: DataFrame contenant les résultats.
    """
    return pd.DataFrame({
        'id': ids,
        'is_fake': y_pred.astype(bool),
        'probability': np.where(y_pred == 1, y_proba[:, 1], y_proba[:, 0]) * 100
    })

def get_download_filename(original_filename):
    """
    Génère un nom de fichier pour le téléchargement des résultats.
    
    Args:
        original_filename (str): Nom du fichier original.
        
    Returns:
        str: Nom du fichier pour le téléchargement.
    """
    if original_filename:
        base_name = original_filename.split('.')[0]
        return f"{base_name}_results.csv"
    return f"billets_results_{SESSION_ID[:8]}.csv"

def merge_dataframes_safely(df1, df2, on, how='inner', df1_name='df1', df2_name='df2'):
    """
    Fusionne deux DataFrames en évitant les conflits de noms de colonnes.
    
    Args:
        df1 (pandas.DataFrame): Premier DataFrame.
        df2 (pandas.DataFrame): Deuxième DataFrame.
        on (str or list): Colonne(s) de jointure.
        how (str): Type de jointure ('inner', 'left', 'right', 'outer').
        df1_name (str): Préfixe pour les colonnes du premier DataFrame en cas de conflit.
        df2_name (str): Préfixe pour les colonnes du deuxième DataFrame en cas de conflit.
        
    Returns:
        pandas.DataFrame: DataFrame fusionné.
    """
    # Identifier les colonnes communes (sauf la/les colonne(s) de jointure)
    on_cols = [on] if isinstance(on, str) else on
    common_cols = set(df1.columns) & set(df2.columns) - set(on_cols)
    
    # Créer des copies pour éviter de modifier les originaux
    df1_copy = df1.copy()
    df2_copy = df2.copy()
    
    # Renommer les colonnes communes dans df2 pour éviter les conflits
    rename_dict = {col: f"{col}_{df2_name}" for col in common_cols}
    df2_copy = df2_copy.rename(columns=rename_dict)
    
    # Fusionner les DataFrames
    merged_df = df1_copy.merge(df2_copy, on=on, how=how)
    
    return merged_df