"""
Création de graphiques radars pour la visualisation des caractéristiques des billets.
"""

import plotly.graph_objects as go
import pandas as pd
from config import BILL_FEATURES, COLORS, get_default_graph_layout

def create_radar_chart(df_data):
    """
    Crée un graphique radar comparant les caractéristiques moyennes des billets authentiques et contrefaits.
    
    Args:
        df_data (pandas.DataFrame): DataFrame contenant les données des billets avec une colonne 'is_fake'.
        
    Returns:
        plotly.graph_objects.Figure: Figure du graphique radar.
    """
    try:
        # Vérifier si la colonne 'is_fake' existe
        if 'is_fake' not in df_data.columns:
            # Message d'erreur si 'is_fake' manque
            fig = go.Figure()
            fig.add_annotation(
                text="Données incomplètes: la colonne 'is_fake' est manquante",
                showarrow=False,
                font=dict(size=14)
            )
            fig.update_layout(height=450)
            return fig
        
        # Créer une copie du DataFrame pour éviter de modifier l'original
        df_numeric = df_data.copy()
        
        # S'assurer que la colonne 'is_fake' est de type booléen
        if not pd.api.types.is_bool_dtype(df_numeric['is_fake']):
            df_numeric['is_fake'] = df_numeric['is_fake'].astype(bool)
        
        # S'assurer que les colonnes à visualiser sont numériques
        available_features = []
        for feature in BILL_FEATURES:
            if feature in df_numeric.columns:
                # Convertir en numérique et remplacer les erreurs par NaN
                df_numeric[feature] = pd.to_numeric(df_numeric[feature], errors='coerce')
                # Si la colonne contient des données numériques valides, l'ajouter à la liste
                if not df_numeric[feature].isna().all():
                    available_features.append(feature)
        
        # Vérifier s'il y a des caractéristiques disponibles
        if not available_features:
            fig = go.Figure()
            fig.add_annotation(
                text="Aucune caractéristique numérique disponible",
                showarrow=False,
                font=dict(size=14)
            )
            fig.update_layout(height=450)
            return fig
        
        # Supprimer les lignes avec des valeurs manquantes dans les caractéristiques disponibles
        df_numeric = df_numeric.dropna(subset=available_features)
        
        # Calculer les moyennes pour chaque dimension par groupe (vrai/faux)
        # Utiliser numeric_only=True pour éviter les erreurs avec les colonnes non numériques
        grouped = df_numeric.groupby('is_fake')[available_features].mean()
        
        # Créer les points pour le graphique radar
        fig = go.Figure()
        
        # Ajouter les données pour les vrais billets
        if False in grouped.index:
            fig.add_trace(go.Scatterpolar(
                r=grouped.loc[False].values.tolist(),
                theta=available_features,
                fill='toself',
                name='Billets authentiques',
                line_color=COLORS['authentic']
            ))
        
        # Ajouter les données pour les faux billets
        if True in grouped.index:
            fig.add_trace(go.Scatterpolar(
                r=grouped.loc[True].values.tolist(),
                theta=available_features,
                fill='toself',
                name='Billets contrefaits',
                line_color=COLORS['fake']
            ))
        
        # Configurer la mise en page
        max_value = df_numeric[available_features].max().max() if not df_numeric[available_features].empty else 10
        
        layout = get_default_graph_layout()
        layout.update(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max_value * 1.1]
                )
            ),
            showlegend=True,
            height=450
        )
        
        fig.update_layout(layout)
        
        return fig
    
    except Exception as e:
        print(f"Erreur dans create_radar_chart: {str(e)}")
        fig = go.Figure()
        fig.add_annotation(
            text=f"Erreur lors de la création du graphique radar: {str(e)}",
            showarrow=False,
            font=dict(size=14)
        )
        fig.update_layout(height=450)
        return fig