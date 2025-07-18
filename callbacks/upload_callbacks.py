"""
Callbacks pour gérer l'upload et l'aperçu des fichiers CSV.
"""

from dash import Input, Output, State, html, dash_table
import dash_bootstrap_components as dbc

from utils.helpers import parse_csv_contents, validate_dataframe
from models.model_loader import clf
from config import BILL_FEATURES

def register_upload_callbacks(app):
    """
    Enregistre les callbacks liés à l'upload et l'aperçu des fichiers.
    
    Args:
        app (dash.Dash): Instance de l'application Dash.
    """
    @app.callback(
        [
            Output("data-preview-container", "children"),
            Output("upload-info", "children"),
            Output("analyze-btn-container", "style"),
        ],
        [Input("upload-csv", "contents")],
        [State("upload-csv", "filename")]
    )
    def update_data_preview(contents, filename):
        """
        Met à jour l'aperçu des données et les messages d'information lors de l'upload d'un fichier.
        """
        from utils.helpers import df  # Import à l'intérieur pour éviter les références circulaires
        
        if contents is None:
            return None, None, {"display": "none"}
        
        # Parsing du fichier CSV
        data, error_message = parse_csv_contents(contents, filename)
        if error_message:
            return None, create_error_message(error_message), {"display": "none"}
        
        # Vérification du modèle
        if clf is None:
            return None, create_error_message("Impossible de charger le modèle. Vérifiez l'installation."), {"display": "none"}
        
        # Vérification des colonnes requises et des valeurs manquantes
        required_columns = BILL_FEATURES + ['id']
        is_valid, error_message = validate_dataframe(data, required_columns)
        if not is_valid:
            return None, create_error_message(error_message), {"display": "none"}
        
        # Mise à jour de la variable globale
        import utils.helpers as helpers
        helpers.df = data
        
        # Création de l'aperçu des données
        preview = create_data_preview(data, filename)
        success_message = create_success_message("Fichier valide et prêt pour l'analyse !")
        
        return preview, success_message, {"display": "block"}

def create_data_preview(data, filename):
    """
    Crée un aperçu des données téléchargées.
    
    Args:
        data (pandas.DataFrame): DataFrame contenant les données téléchargées.
        filename (str): Nom du fichier téléchargé.
        
    Returns:
        list: Liste des composants à afficher.
    """
    return [
        html.H4(f"Aperçu des données : {filename}", className="mb-3"),
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        dash_table.DataTable(
                            data=data.head(5).to_dict('records'),
                            columns=[{"name": col, "id": col} for col in data.columns],
                            style_table={"overflowX": "auto"},
                            style_cell={
                                'textAlign': 'center',
                                'padding': '10px',
                                'fontFamily': '"Segoe UI", Arial, sans-serif'
                            },
                            style_header={
                                'backgroundColor': '#f8f9fa',
                                'fontWeight': 'bold',
                                'borderBottom': '1px solid #dee2e6'
                            },
                            style_data_conditional=[
                                {
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': '#f9f9f9'
                                }
                            ],
                            page_size=5,
                        ),
                        
                        html.Div(
                            [
                                html.P(
                                    [
                                        html.Strong("Nombre total de billets : "),
                                        f"{len(data)}"
                                    ],
                                    className="mb-1"
                                ),
                                html.P(
                                    [
                                        html.Strong("Colonnes présentes : "),
                                        ", ".join(data.columns)
                                    ],
                                    className="mb-0 text-break"
                                ),
                            ],
                            className="mt-3 small",
                        ),
                    ]
                ),
            ],
            className="shadow-sm",
        ),
    ]

def create_success_message(message):
    """
    Crée un message de succès.
    
    Args:
        message (str): Message à afficher.
        
    Returns:
        dash_bootstrap_components.Alert: Composant d'alerte de succès.
    """
    return dbc.Alert(
        [
            html.I(className="fas fa-check-circle me-2"),
            message
        ],
        color="success",
        className="mb-0",
    )

def create_error_message(message):
    """
    Crée un message d'erreur.
    
    Args:
        message (str): Message d'erreur à afficher.
        
    Returns:
        dash_bootstrap_components.Alert: Composant d'alerte d'erreur.
    """
    return dbc.Alert(
        [
            html.I(className="fas fa-exclamation-triangle me-2"),
            message
        ],
        color="danger",
        className="mb-0",
    )