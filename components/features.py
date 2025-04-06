"""
Composant pour la section "Comment ça fonctionne" de l'application BilletScan.
"""

import dash_bootstrap_components as dbc
from dash import html

def create_features():
    """
    Crée la section qui explique le fonctionnement de l'application.
    
    Returns:
        dash_bootstrap_components.Container: Composant de fonctionnalités.
    """
    return dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H2("Comment ça fonctionne", className="text-center mb-4"),
                            html.Hr(className="mb-5"),
                        ]
                    )
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                html.Div(
                                    html.I(className="fas fa-upload fa-3x text-primary"),
                                    className="text-center mt-4"
                                ),
                                dbc.CardBody(
                                    [
                                        html.H4("Importer", className="card-title text-center"),
                                        html.P(
                                            "Téléchargez votre fichier CSV contenant les dimensions des billets à analyser.",
                                            className="card-text text-center",
                                        ),
                                    ]
                                ),
                            ],
                            className="h-100 shadow-sm",
                        ),
                        md=4,
                        className="mb-4",
                    ),
                    dbc.Col(
                        dbc.Card(
                            [
                                html.Div(
                                    html.I(className="fas fa-robot fa-3x text-primary"),
                                    className="text-center mt-4"
                                ),
                                dbc.CardBody(
                                    [
                                        html.H4("Analyser", className="card-title text-center"),
                                        html.P(
                                            "Notre algorithme de machine learning analyse les dimensions des billets pour détecter les anomalies.",
                                            className="card-text text-center",
                                        ),
                                    ]
                                ),
                            ],
                            className="h-100 shadow-sm",
                        ),
                        md=4,
                        className="mb-4",
                    ),
                    dbc.Col(
                        dbc.Card(
                            [
                                html.Div(
                                    html.I(className="fas fa-chart-pie fa-3x text-primary"),
                                    className="text-center mt-4"
                                ),
                                dbc.CardBody(
                                    [
                                        html.H4("Visualiser", className="card-title text-center"),
                                        html.P(
                                            "Obtenez des résultats clairs avec des visualisations interactives et des statistiques détaillées.",
                                            className="card-text text-center",
                                        ),
                                    ]
                                ),
                            ],
                            className="h-100 shadow-sm",
                        ),
                        md=4,
                        className="mb-4",
                    ),
                ]
            ),
        ],
        className="py-5 bg-light",
    )