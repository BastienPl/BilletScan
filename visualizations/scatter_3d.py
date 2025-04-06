"""
Création de graphiques 3D pour la visualisation des relations entre caractéristiques et probabilités.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from config import COLORS, FEATURE_LABELS, get_default_graph_layout

def create_3d_scatter(df_data, df_results_data, dim_x, dim_y):
    """
    Crée un graphique 3D montrant la relation entre deux dimensions des billets 
    et leur niveau de confiance.
    
    Args:
        df_data (pandas.DataFrame): DataFrame contenant les données des billets avec une colonne 'is_fake'.
        df_results_data (pandas.DataFrame): DataFrame contenant les résultats de l'analyse.
        dim_x (str): Dimension à utiliser pour l'axe X.
        dim_y (str): Dimension à utiliser pour l'axe Y.
        
    Returns:
        plotly.graph_objects.Figure: Figure du graphique 3D.
    """
    if not dim_x or not dim_y or df_data is None or df_results_data is None:
        # Message par défaut
        fig = go.Figure()
        fig.add_annotation(
            text="Sélectionnez les dimensions X et Y",
            showarrow=False,
            font=dict(size=14)
        )
        fig.update_layout(height=600)
        return fig
    
    # Créer une copie des DataFrames pour éviter de modifier les originaux
    df_data_copy = df_data.copy()
    
    # S'assurer que les colonnes sélectionnées sont numériques
    if dim_x in df_data_copy.columns:
        df_data_copy[dim_x] = pd.to_numeric(df_data_copy[dim_x], errors='coerce')
    if dim_y in df_data_copy.columns:
        df_data_copy[dim_y] = pd.to_numeric(df_data_copy[dim_y], errors='coerce')
    
    # Vérifier si les colonnes sélectionnées sont disponibles et numériques
    if dim_x not in df_data_copy.columns or dim_y not in df_data_copy.columns:
        fig = go.Figure()
        fig.add_annotation(
            text=f"Dimensions non disponibles: {dim_x if dim_x not in df_data_copy.columns else ''} "
                 f"{dim_y if dim_y not in df_data_copy.columns else ''}",
            showarrow=False,
            font=dict(size=14)
        )
        fig.update_layout(height=600)
        return fig
    
    if not pd.api.types.is_numeric_dtype(df_data_copy[dim_x]) or not pd.api.types.is_numeric_dtype(df_data_copy[dim_y]):
        fig = go.Figure()
        fig.add_annotation(
            text="Les dimensions sélectionnées doivent être numériques",
            showarrow=False,
            font=dict(size=14)
        )
        fig.update_layout(height=600)
        return fig
    
    try:
        # Préparer les DataFrames pour la fusion
        # On ne doit conserver que les colonnes nécessaires pour éviter les doublons
        df_results_minimal = df_results_data[['id', 'is_fake', 'probability']].copy()
        
        # Pour df_data, on ne garde que les colonnes id, dim_x et dim_y
        df_data_minimal = df_data_copy[['id']].copy()
        if dim_x in df_data_copy.columns:
            df_data_minimal[dim_x] = df_data_copy[dim_x]
        if dim_y in df_data_copy.columns:
            df_data_minimal[dim_y] = df_data_copy[dim_y]
            
        # Fusion des DataFrames minimaux
        merged_df = df_data_minimal.merge(
            df_results_minimal,
            on='id',
            how='inner'  # Utiliser inner join pour ne garder que les lignes communes
        )
        
        # Supprimer les lignes avec des valeurs manquantes pour les dimensions sélectionnées
        merged_df = merged_df.dropna(subset=[dim_x, dim_y, 'probability'])
        
        # Si le DataFrame fusionné est vide, créer un graphique vide avec un message
        if merged_df.empty:
            fig = go.Figure()
            fig.add_annotation(
                text="Aucune donnée disponible pour les dimensions sélectionnées",
                showarrow=False,
                font=dict(size=14)
            )
            fig.update_layout(height=600)
            return fig
        
        # Créer un graphique 3D avec les deux dimensions et la probabilité
        fig = px.scatter_3d(
            merged_df,
            x=dim_x,
            y=dim_y,
            z='probability',
            color='is_fake',
            color_discrete_map={True: COLORS['fake'], False: COLORS['authentic']},
            opacity=0.7,
            size_max=10,
            height=600,
            labels=FEATURE_LABELS,
            hover_name="id" if "id" in merged_df.columns else None,
        )
        
        layout = get_default_graph_layout()
        layout.update(
            scene = dict(
                xaxis_title=dict(text=dim_x.capitalize().replace('_', ' ')),
                yaxis_title=dict(text=dim_y.capitalize().replace('_', ' ')),
                zaxis_title=dict(text="Niveau de confiance (%)"),
            ),
            margin=dict(l=0, r=0, b=0, t=0)
        )
        
        fig.update_layout(layout)
        
        return fig
        
    except Exception as e:
        print(f"Erreur dans create_3d_scatter: {str(e)}")
        fig = go.Figure()
        fig.add_annotation(
            text=f"Erreur lors de la création du graphique: {str(e)}",
            showarrow=False,
            font=dict(size=14)
        )
        fig.update_layout(height=600)
        return fig