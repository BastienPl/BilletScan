"""
Création de matrices de dispersion pour la visualisation des relations entre caractéristiques.
"""

import plotly.express as px
import plotly.graph_objects as go
from config import COLORS, FEATURE_LABELS, get_default_graph_layout

def create_scatter_matrix(df_data, selected_features):
    """
    Crée une matrice de graphiques de dispersion pour visualiser les relations 
    entre différentes caractéristiques des billets.
    
    Args:
        df_data (pandas.DataFrame): DataFrame contenant les données des billets avec une colonne 'is_fake'.
        selected_features (list): Liste des caractéristiques à inclure dans la matrice.
        
    Returns:
        plotly.graph_objects.Figure: Figure de la matrice de dispersion.
    """
    if not selected_features or len(selected_features) < 2:
        # Message par défaut si pas assez de caractéristiques sélectionnées
        fig = go.Figure()
        fig.add_annotation(
            text="Sélectionnez au moins deux caractéristiques pour comparer",
            showarrow=False,
            font=dict(size=14)
        )
        fig.update_layout(height=500)
        return fig
    
    # Création d'une matrice de graphiques de dispersion
    fig = px.scatter_matrix(
        df_data,
        dimensions=selected_features,
        color="is_fake",
        color_discrete_map={True: COLORS['fake'], False: COLORS['authentic']},
        labels=FEATURE_LABELS,
        hover_data=["id"],
        template="plotly_white"
    )
    
    layout = get_default_graph_layout()
    layout.update(
        height=500,
        font=dict(size=11),
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    fig.update_layout(layout)
    
    fig.update_traces(
        diagonal_visible=False,
        showupperhalf=False
    )
    
    return fig