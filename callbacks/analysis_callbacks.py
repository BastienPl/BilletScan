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
from visualizations import (
    create_radar_chart, 
    create_box_plot, 
    create_scatter_matrix, 
    create_3d_scatter
)
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
            print("Début de l'analyse des billets")
            
            # Préparation des données et prédiction
            # Vérifier si le DataFrame contient la colonne 'id'
            if 'id' not in df.columns:
                print("Colonne 'id' manquante dans le DataFrame")
                return [], "py-5 d-none"
                
            ids = df['id']
            print(f"Nombre d'identifiants: {len(ids)}")
            
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
            print(f"Lignes supprimées à cause de valeurs manquantes: {original_len - new_len}")
            
            # S'il n'y a pas assez de données, retourner une erreur
            if len(X) == 0:
                print("Aucune donnée valide après nettoyage")
                return [], "py-5 d-none"
            
            # Prédiction
            print("Prédiction avec le modèle")
            y_pred, y_proba = predict(X)
            
            if y_pred is None or y_proba is None:
                print("Échec de la prédiction")
                return [], "py-5 d-none"
            
            # Création du DataFrame de résultats
            print("Création du DataFrame de résultats")
            df_results = create_results_dataframe(ids[:len(y_pred)], y_pred, y_proba)
            helpers.df_results = df_results
            
            # Métriques et statistiques
            total_banknotes = len(df)
            fake_banknotes = df_results['is_fake'].sum()
            fake_percentage = (fake_banknotes / total_banknotes) * 100 if total_banknotes > 0 else 0
            print(f"Statistiques: {fake_banknotes} billets contrefaits sur {total_banknotes} ({fake_percentage:.1f}%)")
            
            # Graphique de distribution des probabilités
            print("Création du graphique de distribution")
            fig_distr = create_distribution_chart(df_results)
            
            # Préparer le DataFrame pour les visualisations
            # On crée un DataFrame avec toutes les caractéristiques et le statut is_fake
            print("Préparation des données pour les visualisations")
            df_for_viz = df.copy()
            
            # Ajouter le statut is_fake de df_results
            # Fusionner sur id, les lignes sans correspondance auront des NaN pour is_fake
            print("Fusion des DataFrames pour les visualisations")
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
            print(f"Caractéristiques numériques disponibles: {numeric_cols}")
            
            # Initialiser les graphiques pour l'affichage initial
            initial_features = [f for f in ["margin_low", "length"] if f in numeric_cols]
            if len(initial_features) < 2 and len(numeric_cols) >= 2:
                # Si les caractéristiques initiales ne sont pas disponibles, prendre les deux premières colonnes numériques
                initial_features = numeric_cols[:2]
            
            print(f"Caractéristiques initiales pour la matrice: {initial_features}")
            
            # Création des visualisations
            print("Création des visualisations")
            
            # Création du radar chart
            fig_radar = create_radar_chart(df_for_viz)
            
            # Création du box plot
            fig_boxplot = create_box_plot(df_for_viz)
            
            # Création de la matrice de dispersion
            if len(initial_features) >= 2:
                fig_scatter = create_scatter_matrix(df_for_viz, initial_features)
            else:
                # Créer un graphique vide si pas assez de caractéristiques
                fig_scatter = go.Figure()
                fig_scatter.add_annotation(
                    text="Pas assez de caractéristiques numériques disponibles",
                    showarrow=False,
                    font=dict(size=14)
                )
                fig_scatter.update_layout(height=500)
            
            # Création du graphique 3D
            # Pour le graphique 3D, choisir deux dimensions numériques disponibles
            dim_x = numeric_cols[0] if len(numeric_cols) > 0 else None
            dim_y = numeric_cols[1] if len(numeric_cols) > 1 else dim_x
            
            fig_3d = create_3d_scatter(df_for_viz, df_results, dim_x, dim_y)
            
            # Création du DataFrame pour le tableau de résultats - toutes les données fusionnées
            print("Préparation des données pour le tableau de résultats")
            df_results_with_features = df_results.merge(
                df, 
                on='id',
                how='inner'
            )
            
            # Création des résultats
            print("Création du contenu des résultats")
            results_content = create_results_content(
                total_banknotes, 
                fake_banknotes, 
                fake_percentage, 
                filename, 
                fig_distr, 
                fig_radar, 
                fig_boxplot, 
                fig_scatter, 
                fig_3d, 
                df_results_with_features,
                initial_features
            )
            
            print("Analyse terminée avec succès")
            return results_content, "py-5"
            
        except Exception as e:
            print(f"Erreur lors de l'analyse: {str(e)}")
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
            print(f"Mise à jour du graphique 3D avec dimensions: {dim_x}, {dim_y}")
            from utils.helpers import df, df_results
            
            if df is None or df_results is None or not dim_x or not dim_y:
                print("Pas assez de données ou dimensions pour le graphique 3D")
                fig = go.Figure()
                fig.add_annotation(
                    text="Veuillez sélectionner les dimensions X et Y",
                    showarrow=False,
                    font=dict(size=14)
                )
                fig.update_layout(height=600)
                return fig
                
            # Fusion avec df_results pour avoir la colonne is_fake
            print("Fusion des données pour la mise à jour du graphique 3D")
            df_with_results = df.copy()
            df_with_results = df_with_results.merge(
                df_results[['id', 'is_fake']],
                on='id',
                how='left'
            )
                
            print("Création du graphique 3D mis à jour")
            return create_3d_scatter(df_with_results, df_results, dim_x, dim_y)
            
        except Exception as e:
            print(f"Erreur lors de la mise à jour du graphique 3D: {str(e)}")
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
        Output("download-results", "data"),
        [Input("btn-download-csv", "n_clicks")],
        [State("upload-csv", "filename")]
    )
    def download_results(n_clicks, filename):
        """
        Télécharge les résultats au format CSV.
        """
        try:
            from utils.helpers import df, df_results
            
            if n_clicks is None or n_clicks == 0 or df is None or df_results is None:
                return None
            
            print("Préparation des résultats pour le téléchargement")
            # Fusion des DataFrames pour créer le fichier de résultats
            results_df = df_results.merge(
                df, 
                on='id',
                how='inner'
            )
            
            # Création d'un nom de fichier pour le téléchargement
            download_filename = get_download_filename(filename)
            print(f"Téléchargement du fichier: {download_filename}")
            
            # Retourner les données pour le téléchargement
            return dcc.send_data_frame(results_df.to_csv, download_filename, index=False)
            
        except Exception as e:
            print(f"Erreur lors du téléchargement des résultats: {str(e)}")
            traceback.print_exc()
            return None
    
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

def create_distribution_chart(df_results):
    """
    Crée un graphique de distribution des niveaux de confiance.
    
    Args:
        df_results (pandas.DataFrame): DataFrame contenant les résultats de l'analyse.
        
    Returns:
        plotly.graph_objects.Figure: Figure du graphique de distribution.
    """
    try:
        print("Création du graphique de distribution")
        print(f"Colonnes dans df_results: {df_results.columns.tolist()}")
        
        # S'assurer que les colonnes nécessaires existent
        if 'probability' not in df_results.columns or 'is_fake' not in df_results.columns:
            missing_cols = []
            if 'probability' not in df_results.columns:
                missing_cols.append('probability')
            if 'is_fake' not in df_results.columns:
                missing_cols.append('is_fake')
            
            print(f"Colonnes manquantes: {missing_cols}")
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
            print(f"Conversion de 'is_fake' en bool - valeurs uniques: {df_results_clean['is_fake'].unique()}")
            df_results_clean['is_fake'] = df_results_clean['is_fake'].astype(bool)
        
        # S'assurer que la colonne 'probability' est numérique
        df_results_clean['probability'] = pd.to_numeric(df_results_clean['probability'], errors='coerce')
        
        # Afficher des statistiques
        print(f"Valeurs NaN dans 'probability': {df_results_clean['probability'].isna().sum()}/{len(df_results_clean)}")
        
        # Supprimer les lignes avec des valeurs manquantes
        original_len = len(df_results_clean)
        df_results_clean = df_results_clean.dropna(subset=['probability'])
        new_len = len(df_results_clean)
        print(f"Lignes supprimées à cause de valeurs manquantes: {original_len - new_len}")
        
        # Si le DataFrame est vide après suppression des NaN, créer un graphique vide
        if df_results_clean.empty:
            print("DataFrame vide après suppression des NaN")
            fig = go.Figure()
            fig.add_annotation(
                text="Aucune donnée valide disponible pour la distribution",
                showarrow=False,
                font=dict(size=14)
            )
            fig.update_layout(height=400)
            return fig
        
        # Statistiques de base
        print(f"Statistiques de probabilité: min={df_results_clean['probability'].min()}, max={df_results_clean['probability'].max()}, mean={df_results_clean['probability'].mean()}")
        
        # Vérifier les valeurs uniques de is_fake
        is_fake_values = df_results_clean['is_fake'].unique()
        print(f"Valeurs uniques de is_fake: {is_fake_values}")
        
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
        
        print("Graphique de distribution créé avec succès")
        return fig
        
    except Exception as e:
        print(f"Erreur dans create_distribution_chart: {str(e)}")
        import traceback
        traceback.print_exc()
        fig = go.Figure()
        fig.add_annotation(
            text=f"Erreur lors de la création du graphique de distribution: {str(e)}",
            showarrow=False,
            font=dict(size=14)
        )
        fig.update_layout(height=400)
        return fig