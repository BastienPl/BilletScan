"""
Callbacks pour gérer l'analyse des billets et l'affichage des résultats.
"""

from dash import Input, Output, State, dcc
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from models.model_loader import predict
from components.results import create_results_content
from utils.helpers import create_results_dataframe, get_download_filename
from visualizations.echarts_charts import get_echarts_bar_options
from config import COLORS, BILL_FEATURES

# Importation nécessaire pour le graphique de distribution corrigé
import traceback

def register_analysis_callbacks(app):
    """
    Enregistre les callbacks liés à l'analyse et aux visualisations.
    
    Args:
        app (dash.Dash): Instance de l'application Dash.
    """
    @app.callback(
        Output("results-container", "children"),
        Output("results-container", "className"),
        [Input("analyze-btn", "n_clicks")],
        [State("upload-csv", "filename")]
    )
    def analyze_banknotes(n_clicks, filename):
        """
        Analyse les billets et affiche les résultats.
        """
        # Import à l'intérieur pour éviter les références circulaires
        from utils.helpers import df
        import utils.helpers as helpers
        
        if n_clicks is None or n_clicks == 0 or df is None:
            return [], "py-5 d-none"
        
        try:
            
            # Préparation des données et prédiction
            # Vérifier si le DataFrame contient la colonne 'id'
            if 'id' not in df.columns:
                return [], "py-5 d-none"
                
            ids = df['id']
            
            # Créer une copie du DataFrame pour la prédiction
            X = df.copy()
            
            # S'assurer que les caractéristiques sont numériques
            for feature in BILL_FEATURES:
                if feature in X.columns:
                    X[feature] = pd.to_numeric(X[feature], errors='coerce')
            
            # Supprimer la colonne 'id' pour la prédiction
            if 'id' in X.columns:
                X = X.drop(columns='id')
                
            # Si la colonne 'is_fake' existe déjà, la supprimer pour éviter la confusion
            if 'is_fake' in X.columns:
                X = X.drop(columns='is_fake')
            
            # Supprimer les lignes avec des valeurs manquantes
            original_len = len(X)
            X = X.dropna()
            new_len = len(X)
            
            # S'il n'y a pas assez de données, retourner une erreur
            if len(X) == 0:
                return [], "py-5 d-none"
            
            # Prédiction
            y_pred, y_proba = predict(X)
            
            if y_pred is None or y_proba is None:
                return [], "py-5 d-none"
            
            # Création du DataFrame de résultats
            df_results = create_results_dataframe(ids[:len(y_pred)], y_pred, y_proba)
            helpers.df_results = df_results
            
            # Métriques et statistiques
            total_banknotes = len(df)
            fake_banknotes = df_results['is_fake'].sum()
            fake_percentage = (fake_banknotes / total_banknotes) * 100 if total_banknotes > 0 else 0
            
            # Graphique de distribution des probabilités
            fig_distr = create_distribution_chart(df_results)
            
            # Préparer le DataFrame pour les visualisations
            # On crée un DataFrame avec toutes les caractéristiques et le statut is_fake
            df_for_viz = df.copy()
            
            # Ajouter le statut is_fake de df_results
            # Fusionner sur id, les lignes sans correspondance auront des NaN pour is_fake
            df_for_viz = df_for_viz.merge(
                df_results[['id', 'is_fake']],
                on='id',
                how='left'
            )
            
            # Convertir les caractéristiques en numériques
            for feature in BILL_FEATURES:
                if feature in df_for_viz.columns:
                    df_for_viz[feature] = pd.to_numeric(df_for_viz[feature], errors='coerce')
            
            # Trouver les caractéristiques numériques disponibles
            numeric_cols = [col for col in df_for_viz.columns 
                           if col in BILL_FEATURES and pd.api.types.is_numeric_dtype(df_for_viz[col])]
            
            # Initialiser les graphiques pour l'affichage initial
            initial_features = [f for f in ["margin_low", "length"] if f in numeric_cols]
            if len(initial_features) < 2 and len(numeric_cols) >= 2:
                # Si les caractéristiques initiales ne sont pas disponibles, prendre les deux premières colonnes numériques
                initial_features = numeric_cols[:2]
            
            # Création des visualisations SIMPLIFIÉES
            # On choisit 'length' comme caractéristique par défaut pour le barplot
            feature_for_bar = 'length' if 'length' in df_for_viz.columns else (numeric_cols[0] if numeric_cols else None)
            fig_bar = go.Figure() # create_barplot_feature(df_for_viz, feature=feature_for_bar) if feature_for_bar else go.Figure()

            # Préparation des données pour le tableau de résultats - toutes les données fusionnées
            df_results_with_features = df_results.merge(
                df, 
                on='id',
                how='inner'
            )

            # Création des résultats SIMPLIFIÉS
            # Liste des colonnes numériques disponibles pour la dropdown
            numeric_cols = [col for col in df_for_viz.columns if col in BILL_FEATURES and pd.api.types.is_numeric_dtype(df_for_viz[col])]
            selected_bar_features = ['length'] if 'length' in numeric_cols else (numeric_cols[:1] if numeric_cols else [])
            # Appel corrigé à create_results_content (version ECharts)
            results_content = create_results_content(
                total_banknotes, 
                fake_banknotes, 
                fake_percentage, 
                filename, 
                df_results_with_features,
                numeric_cols,
                selected_bar_features
            )
            
            return results_content, "py-5"
            
        except Exception as e:
            traceback.print_exc()
            return [], "py-5 d-none"
    
    @app.callback(
        Output("scatter-matrix", "figure"),
        [Input("feature-checklist", "value")]
    )
    def update_scatter_matrix(selected_features):
        try:
            # Message de débogage visible dans l'interface
            fig = go.Figure()
            fig.add_annotation(
                text=f"Tentative de création de matrice avec: {selected_features}",
                showarrow=False,
                font=dict(size=14)
            )
            fig.update_layout(height=500)
            
            # Redirection vers console navigateur
            fig.add_annotation(
                text="Vérifiez la console du navigateur (F12) pour les détails",
                y=0.4,
                showarrow=False,
                font=dict(size=12)
            )
            
            # Code pour ajouter un message dans la console du navigateur
            fig.add_annotation(
                text="console.log('Débogage scatter matrix: ' + JSON.stringify("+str(selected_features)+"));",
                visible=False,
                showarrow=False,
                font=dict(size=1),
                jsfunction=True
            )
            
            return fig
        except Exception as e:
            fig = go.Figure()
            fig.add_annotation(
                text=f"Erreur: {str(e)}",
                showarrow=False,
                font=dict(size=14)
            )
            fig.update_layout(height=500)
            return fig
    
    @app.callback(
        Output("3d-scatter", "figure"),
        [Input("dim-x-dropdown", "value"),
         Input("dim-y-dropdown", "value")]
    )
    def update_3d_scatter(dim_x, dim_y):
        """
        Met à jour le graphique 3D en fonction des dimensions sélectionnées.
        """
        try:
            from utils.helpers import df, df_results
            
            if df is None or df_results is None or not dim_x or not dim_y:
                fig = go.Figure()
                fig.add_annotation(
                    text="Veuillez sélectionner les dimensions X et Y",
                    showarrow=False,
                    font=dict(size=14)
                )
                fig.update_layout(height=600)
                return fig
                
            # Fusion avec df_results pour avoir la colonne is_fake
            df_with_results = df.copy()
            df_with_results = df_with_results.merge(
                df_results[['id', 'is_fake']],
                on='id',
                how='left'
            )
                
            return go.Figure() # create_3d_scatter(df_with_results, df_results, dim_x, dim_y)
            
        except Exception as e:
            traceback.print_exc()
            fig = go.Figure()
            fig.add_annotation(
                text=f"Erreur: {str(e)}",
                showarrow=False,
                font=dict(size=14)
            )
            fig.update_layout(height=600)
            return fig
    
    @app.callback(
        Output('download-results', 'data'),
        [Input('btn-download-csv', 'n_clicks')],
        [State('results-table', 'data'), State('upload-csv', 'filename')]
    )
    def download_results(n_clicks, table_data, filename):
        import pandas as pd
        if not n_clicks or not table_data:
            return dcc.no_update
        df = pd.DataFrame(table_data)
        # Nom du fichier basé sur le nom du fichier uploadé
        base = filename.rsplit('.', 1)[0] if filename else 'resultats'
        return dcc.send_data_frame(df.to_csv, f"{base}_resultats.csv", index=False, sep=';')
    
    @app.callback(
        Output("navbar-collapse", "is_open"),
        [Input("navbar-toggler", "n_clicks")],
        [State("navbar-collapse", "is_open")],
    )
    def toggle_navbar_collapse(n, is_open):
        """
        Ouvre/ferme le menu de navigation sur mobile.
        """
        if n:
            return not is_open
        return is_open

    # Nouveau callback pour le barplot dynamique
    @app.callback(
        Output('echarts-bar', 'option'),
        [Input('barplot-feature-dropdown', 'value')],
        [State('results-table', 'data')]
    )
    def update_barplot_echarts(selected_features, table_data):
        import pandas as pd
        if not selected_features or not table_data:
            return {}
        df = pd.DataFrame(table_data)
        if 'is_fake' not in df.columns:
            return {}
        return get_echarts_bar_options(df, selected_features)

def create_distribution_chart(df_results):
    """
    Crée un graphique de distribution des niveaux de confiance.
    
    Args:
        df_results (pandas.DataFrame): DataFrame contenant les résultats de l'analyse.
        
    Returns:
        plotly.graph_objects.Figure: Figure du graphique de distribution.
    """
    try:
        
        # S'assurer que les colonnes nécessaires existent
        if 'probability' not in df_results.columns or 'is_fake' not in df_results.columns:
            missing_cols = []
            if 'probability' not in df_results.columns:
                missing_cols.append('probability')
            if 'is_fake' not in df_results.columns:
                missing_cols.append('is_fake')
            
            fig = go.Figure()
            fig.add_annotation(
                text=f"Données incomplètes: colonnes manquantes {', '.join(missing_cols)}",
                showarrow=False,
                font=dict(size=14)
            )
            fig.update_layout(height=400)
            return fig
        
        # S'assurer que la colonne 'is_fake' est de type booléen
        df_results_clean = df_results.copy()
        if not pd.api.types.is_bool_dtype(df_results_clean['is_fake']):
            df_results_clean['is_fake'] = df_results_clean['is_fake'].astype(bool)
        
        # S'assurer que la colonne 'probability' est numérique
        df_results_clean['probability'] = pd.to_numeric(df_results_clean['probability'], errors='coerce')
        
        # Afficher des statistiques
        
        # Supprimer les lignes avec des valeurs manquantes
        original_len = len(df_results_clean)
        df_results_clean = df_results_clean.dropna(subset=['probability'])
        new_len = len(df_results_clean)
        
        # Si le DataFrame est vide après suppression des NaN, créer un graphique vide
        if df_results_clean.empty:
            fig = go.Figure()
            fig.add_annotation(
                text="Aucune donnée valide disponible pour la distribution",
                showarrow=False,
                font=dict(size=14)
            )
            fig.update_layout(height=400)
            return fig
        
        # Statistiques de base
        
        # Vérifier les valeurs uniques de is_fake
        
        # Création du graphique
        fig = px.histogram(
            df_results_clean, 
            x="probability", 
            color="is_fake", 
            nbins=20,
            labels={"probability": "Niveau de confiance (%)", "is_fake": "Billet contrefait"},
            color_discrete_map={True: COLORS['fake'], False: COLORS['authentic']},
            template="plotly_white"
        )
        
        fig.update_layout(
            title="Distribution des niveaux de confiance",
            xaxis_title="Niveau de confiance (%)",
            yaxis_title="Nombre de billets",
            legend_title="Statut",
            showlegend=True,
            height=400
        )
        
        return fig
        
    except Exception as e:
        traceback.print_exc()
        fig = go.Figure()
        fig.add_annotation(
            text=f"Erreur lors de la création du graphique de distribution: {str(e)}",
            showarrow=False,
            font=dict(size=14)
        )
        fig.update_layout(height=400)
        return fig