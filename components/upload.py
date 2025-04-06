"""
Composant pour la section d'upload et d'aperçu des données de l'application BilletScan.
"""

import dash_bootstrap_components as dbc
from dash import html, dcc

def create_upload():
    """
    Crée la section pour télécharger et prévisualiser les fichiers CSV.
    
    Returns:
        dash_bootstrap_components.Container: Composant d'upload.
    """
    return dbc.Container(
        id="upload-section",
        children=[
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H2("Analyser vos billets", className="mb-4"),
                            html.P(
                                "Téléchargez votre fichier CSV contenant les dimensions des billets pour commencer l'analyse.",
                                className="lead"
                            ),
                            html.Hr(className="my-4"),
                            dcc.Upload(
                                id="upload-csv",
                                children=dbc.Card(
                                    [
                                        html.Div(
                                            html.I(className="fas fa-cloud-upload-alt fa-4x text-primary"),
                                            className="text-center mt-4"
                                        ),
                                        dbc.CardBody(
                                            [
                                                html.H5("Glisser-déposer", className="card-title text-center"),
                                                html.P(
                                                    "ou cliquez pour sélectionner un fichier CSV",
                                                    className="card-text text-center text-muted",
                                                ),
                                            ]
                                        ),
                                    ],
                                    className="border-dashed border-2 h-100",
                                    style={"borderStyle": "dashed", "cursor": "pointer"},
                                ),
                                style={"height": "250px"},
                                multiple=False,
                            ),
                            
                            # Messages d'information
                            html.Div(id="upload-info", className="mt-4"),
                            
                            # Bouton d'analyse (initialement caché)
                            html.Div(
                                dbc.Button(
                                    [
                                        html.I(className="fas fa-search-dollar me-2"),
                                        "Analyser les billets"
                                    ],
                                    id="analyze-btn",
                                    size="lg",
                                    className="mt-3 w-100 btn-primary",
                                    n_clicks=0,
                                ),
                                id="analyze-btn-container",
                                style={"display": "none"},
                            ),
                        ],
                        md=5,
                        className="mb-4",
                    ),
                    dbc.Col(
                        [
                            # Aperçu des données
                            html.Div(id="data-preview-container", className="h-100"),
                        ],
                        md=7,
                        className="mb-4",
                    ),
                ]
            ),
        ],
        className="py-5",
    )