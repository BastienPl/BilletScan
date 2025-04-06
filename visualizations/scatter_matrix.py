"""
Création de matrices de dispersion pour la visualisation des relations entre caractéristiques.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from config import COLORS, FEATURE_LABELS, get_default_graph_layout

# Modification simplifiée pour visualizations/scatter_matrix.py
def create_scatter_matrix(df_data, selected_features):
    """Version simplifiée pour le débogage"""
    try:
        # Créer un petit DataFrame test avec des données numériques connues
        test_data = pd.DataFrame({
            'feature1': [1, 2, 3, 4, 5],
            'feature2': [5, 4, 3, 2, 1],
            'is_fake': [True, False, True, False, True]
        })
        
        # Utiliser ce DataFrame test pour la matrice
        fig = px.scatter_matrix(
            test_data,
            dimensions=['feature1', 'feature2'],
            color='is_fake',
            color_discrete_map={True: COLORS['fake'], False: COLORS['authentic']},
            template="plotly_white"
        )
        
        # Configuration simplifiée
        fig.update_layout(height=500)
        
        return fig
        
    except Exception as e:
        print(f"Erreur: {str(e)}")
        fig = go.Figure()
        fig.add_annotation(
            text=f"Erreur: {str(e)}",
            showarrow=False,
            font=dict(size=14)
        )
        fig.update_layout(height=500)
        return fig