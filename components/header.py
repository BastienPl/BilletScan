"""
Composant d'en-tête pour l'application BilletScan.
"""

import dash_bootstrap_components as dbc
from dash import html

def create_header(app):
    """
    Crée l'en-tête de l'application avec le titre, la description et un bouton d'action.
    
    Args:
        app (dash.Dash): Instance de l'application Dash.
        
    Returns:
        dash_bootstrap_components.Container: Composant d'en-tête.
    """
    return dbc.Container(
        children=[
            dbc.Row(
                dbc.Col(
                    [
                        html.H1("Détection de faux billets", className="display-4 fw-bold text-center"),
                        html.P(
                            "Une solution basée sur l'intelligence artificielle pour identifier les billets contrefaits avec précision.",
                            className="lead fs-4 text-center"
                        ),
                        dbc.Button(
                            "Commencer l'analyse", 
                            color="primary", 
                            size="lg", 
                            id="start-btn",
                            href="#upload-section",
                            className="mt-3 d-block mx-auto"  # Centrer le bouton
                        ),
                    ],
                    className="py-5 d-flex flex-column justify-content-center",
                    md=12,  # Utiliser toute la largeur de l'écran
                )
            ),
        ],
        className="py-4",
    )