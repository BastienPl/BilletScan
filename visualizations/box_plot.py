"""
Création de boîtes à moustaches pour la visualisation des caractéristiques des billets.
"""

import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots
from config import BILL_FEATURES, COLORS, get_default_graph_layout

def create_box_plot(df_data):
    """
    Crée un ensemble de boîtes à moustaches pour comparer la distribution 
    des caractéristiques entre billets authentiques et contrefaits.
    
    Args:
        df_data (pandas.DataFrame): DataFrame contenant les données des billets avec une colonne 'is_fake'.
        
    Returns:
        plotly.graph_objects.Figure: Figure avec les boîtes à moustaches.
    """
    # Créer une copie du DataFrame pour éviter de modifier l'original
    df_numeric = df_data.copy()
    
    # S'assurer que les colonnes à visualiser sont numériques
    for feature in BILL_FEATURES:
        if feature in df_numeric.columns:
            # Convertir en numérique et remplacer les erreurs par NaN
            df_numeric[feature] = pd.to_numeric(df_numeric[feature], errors='coerce')
    
    # Vérifions quelles caractéristiques sont effectivement disponibles et numériques
    available_features = [f for f in BILL_FEATURES if f in df_numeric.columns and pd.api.types.is_numeric_dtype(df_numeric[f])]
    
    # S'il n'y a pas de caractéristiques numériques disponibles, créer un graphique vide avec un message
    if not available_features:
        fig = go.Figure()
        fig.add_annotation(
            text="Aucune caractéristique numérique disponible pour créer les boîtes à moustaches",
            showarrow=False,
            font=dict(size=14)
        )
        fig.update_layout(height=550)
        return fig
    
    # Créer la figure avec des sous-graphiques
    # Ajuster le nombre de lignes et colonnes en fonction du nombre de caractéristiques disponibles
    num_rows = (len(available_features) + 2) // 3  # Arrondir à l'entier supérieur pour le nombre de lignes
    num_cols = min(3, len(available_features))  # Maximum 3 colonnes
    
    fig = make_subplots(
        rows=num_rows, 
        cols=num_cols,
        subplot_titles=available_features,
        shared_yaxes=False
    )
    
    # Créer une liste de positions pour les caractéristiques
    positions = {}
    for i, feature in enumerate(available_features):
        positions[feature] = (i // num_cols + 1, i % num_cols + 1)
    
    # Ajouter les boîtes pour chaque caractéristique
    for feature, (row, col) in positions.items():
        # S'assurer que les données pour cette caractéristique ne sont pas vides
        if feature not in df_numeric.columns:
            continue
            
        # Boxplot pour les vrais billets
        authentic_data = df_numeric[df_numeric['is_fake'] == False][feature].dropna()
        if len(authentic_data) > 0:
            fig.add_trace(
                go.Box(
                    y=authentic_data,
                    name='Authentiques',
                    marker_color=COLORS['authentic'],
                    showlegend=True if row == 1 and col == 1 else False
                ),
                row=row, col=col
            )
        
        # Boxplot pour les faux billets
        fake_data = df_numeric[df_numeric['is_fake'] == True][feature].dropna()
        if len(fake_data) > 0:
            fig.add_trace(
                go.Box(
                    y=fake_data,
                    name='Contrefaits',
                    marker_color=COLORS['fake'],
                    showlegend=True if row == 1 and col == 1 else False
                ),
                row=row, col=col
            )
    
    # Mettre à jour la mise en page
    layout = get_default_graph_layout()
    layout.update(
        height=550,
        boxmode='group'
    )
    
    fig.update_layout(layout)
    
    return fig