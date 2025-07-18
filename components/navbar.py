"""
Composant de barre de navigation pour l'application BilletScan.
"""

import dash_bootstrap_components as dbc
from dash import html

def create_navbar(app):
    """
    Crée la barre de navigation de l'application.
    
    Args:
        app (dash.Dash): Instance de l'application Dash.
        
    Returns:
        dash_bootstrap_components.Navbar: Composant de barre de navigation.
    """
    return dbc.Navbar(
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            html.Img(src=app.get_asset_url("billet-de-banque.png"), height="40px"),
                            className="me-2",
                        ),
                        dbc.Col(
                            dbc.NavbarBrand("BilletScan", className="ms-2 fw-bold fs-3"),
                        ),
                    ],
                    align="center",
                    className="g-0",
                ),
                dbc.Nav(
                    [
                        html.Img(src=app.get_asset_url("logo_ocr.png"), className="img-fluid", style={"height": "50px", "width": "auto"})
                    ],
                    className="ms-auto",
                    navbar=True,
                ),
            ]
        ),
        color="primary",
        dark=True,
        className="mb-4",
    )