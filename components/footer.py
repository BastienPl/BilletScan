"""
Composant de pied de page pour l'application BilletScan.
"""

import dash_bootstrap_components as dbc
from dash import html

def create_footer():
    """
    Crée le pied de page de l'application.
    
    Returns:
        dash_bootstrap_components.Container: Composant de pied de page.
    """
    return dbc.Container(
        fluid=True,
        className="bg-dark text-white py-4 mt-5 px-0",
        children=[
            dbc.Container(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.H5("BilletScan", className="mb-3"),
                                    html.P(
                                        "Solution de détection de faux billets basée sur l'apprentissage automatique.",
                                        className="small"
                                    ),
                                ],
                                md=4,
                            ),
                            dbc.Col(
                                [
                                    html.H5("Contact", className="mb-3"),
                                    html.P(
                                        [
                                            html.I(className="fas fa-envelope me-2"),
                                            "pieplubastien@gmail.com",
                                        ],
                                        className="small"
                                    )
                                ],
                                md=4,
                            )
                        ]
                    ),
                    html.Hr(),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.P(
                                    "© 2025 BilletScan par Bastien Pieplu. Tous droits réservés.",
                                    className="text-center small mb-0"
                                ),
                            ),
                        ]
                    ),
                ]
            ),
        ],
    )