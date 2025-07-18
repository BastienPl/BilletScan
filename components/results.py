"""
Composant pour afficher les résultats de l'analyse des billets.
"""

import dash_bootstrap_components as dbc
from dash import html, dcc
from dash_echarts import DashECharts
from visualizations.echarts_charts import get_echarts_pie_options, get_echarts_hist_options, get_echarts_bar_options, get_echarts_radar_options

def create_results():
    """
    Crée la section pour afficher les résultats de l'analyse.
    Cette section est initialement masquée et sera remplie dynamiquement.
    
    Returns:
        dash_bootstrap_components.Container: Composant de résultats.
    """
    return dbc.Container(
        id="results-container",
        children=[],
        className="py-5 d-none",
    )

def create_results_content(total_banknotes, fake_banknotes, fake_percentage, filename, 
                          df_results_with_features, numeric_cols=None, selected_bar_features=None):
    """
    Génère le contenu à afficher dans la section des résultats après analyse.
    Version améliorée : chaque graphique dans une card, barplot dynamique.
    """
    if numeric_cols is None:
        numeric_cols = [
            'diagonal', 'height_left', 'height_right', 'margin_low', 'margin_up', 'length'
        ]
    if selected_bar_features is None:
        selected_bar_features = ['length']
    # Génération des options ECharts
    pie_options = get_echarts_pie_options(df_results_with_features)
    hist_options = get_echarts_hist_options(df_results_with_features)
    bar_options = get_echarts_bar_options(df_results_with_features, selected_bar_features)
    radar_options = get_echarts_radar_options(df_results_with_features, numeric_cols)
    return [
        dbc.Row([
            dbc.Col(html.H2("Résultats de l'analyse", className="mb-4 text-primary text-center"), width=12),
        ], className="mb-4"),
        # Cartes de statistiques
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H3(total_banknotes, className="card-title text-center display-4"),
                    html.P("Billets analysés", className="card-text text-center text-muted"),
                ]),
                dbc.CardFooter(html.Small(f"Fichier : {filename}", className="text-muted")),
            ], className="text-center h-100 shadow-sm"), md=4, className="mb-4"),
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H3(fake_banknotes, className="card-title text-center display-4 text-danger" if fake_banknotes > 0 else "card-title text-center display-4 text-success"),
                    html.P("Faux billets détectés", className="card-text text-center text-muted"),
                ]),
                dbc.CardFooter(html.Small([
                    html.I(className="fas fa-exclamation-triangle me-1 text-danger" if fake_banknotes > 0 else "fas fa-check-circle me-1 text-success"),
                    f"{fake_percentage:.1f}% des billets analysés"
                ], className="text-muted")),
            ], className="text-center h-100 shadow-sm", color="danger" if fake_banknotes > 0 else "success", outline=True), md=4, className="mb-4"),
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H3(f"{df_results_with_features['probability'].mean():.1f}%", className="card-title text-center display-4"),
                    html.P("Niveau de confiance moyen", className="card-text text-center text-muted"),
                ]),
                dbc.CardFooter(html.Small([
                    html.I(className="fas fa-chart-line me-1"),
                    f"Min: {df_results_with_features['probability'].min():.1f}% | Max: {df_results_with_features['probability'].max():.1f}%"
                ], className="text-muted")),
            ], className="text-center h-100 shadow-sm"), md=4, className="mb-4"),
        ], className="mb-4"),
        # Graphiques ECharts dans deux lignes de deux colonnes
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader(html.H5("Répartition des billets (camembert)", className="mb-0 text-center")),
                dbc.CardBody(DashECharts(
                    option=pie_options,
                    style={"height": "350px", "width": "100%"},
                    id="echarts-pie"
                )),
            ]), md=6, className="mb-4"),
            dbc.Col(dbc.Card([
                dbc.CardHeader(html.H5("Distribution des probabilités", className="mb-0 text-center")),
                dbc.CardBody(DashECharts(
                    option=hist_options,
                    style={"height": "350px", "width": "100%"},
                    id="echarts-hist"
                )),
            ]), md=6, className="mb-4"),
        ], className="g-4 justify-content-center align-items-stretch"),
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader([
                    html.H5("Comparaison des variables", className="mb-0 text-center"),
                    dcc.Dropdown(
                        id="barplot-feature-dropdown",
                        options=[{"label": f, "value": f} for f in numeric_cols],
                        value=selected_bar_features,
                        multi=True,
                        clearable=False,
                        className="mt-2 mb-2"
                    ),
                ]),
                dbc.CardBody(DashECharts(
                    option=bar_options,
                    style={"height": "350px", "width": "100%"},
                    id="echarts-bar"
                )),
            ]), md=6, className="mb-4"),
            dbc.Col(dbc.Card([
                dbc.CardHeader(html.H5("Profil moyen (Radar chart)", className="mb-0 text-center")),
                dbc.CardBody(DashECharts(
                    option=radar_options,
                    style={"height": "350px", "width": "100%"},
                    id="echarts-radar"
                )),
            ]), md=6, className="mb-4"),
        ], className="g-4 justify-content-center align-items-stretch"),
        # Tableau de résultats
        dbc.Row([
            dbc.Col([
                html.H4("Tableau des résultats", className="mb-3 mt-4 text-center text-secondary"),
                create_results_table(df_results_with_features),
                html.Div([
                    dbc.Button([
                        html.I(className="fas fa-download me-2"),
                        "Télécharger les résultats (CSV)"
                    ], id="btn-download-csv", color="primary", outline=True, size="sm", className="mt-3 mb-4"),
                ], className="d-flex justify-content-end"),
            ], width=12)
        ], className="mb-4"),
    ]

from dash import dash_table
from dash.dash_table.Format import Format, Scheme

def create_results_table(df):
    """
    Crée un tableau de données à partir du DataFrame des résultats.

    Args:
        df (pandas.DataFrame): DataFrame contenant les résultats.

    Returns:
        dash_table.DataTable: Composant de tableau de données.
    """

    # Vérification des colonnes requises
    expected_columns = {"id", "is_fake", "probability", "diagonal", "height_left", 
                        "height_right", "margin_low", "margin_up", "length"}
    missing_columns = expected_columns - set(df.columns)
    if missing_columns:
        raise ValueError(f"Colonnes manquantes dans le DataFrame : {missing_columns}")

    return dash_table.DataTable(
        id='results-table',
        data=df.to_dict('records'),
        columns=[
            {"name": "ID", "id": "id"},
            {"name": "Contrefait", "id": "is_fake"},
            {"name": "Confiance (%)", "id": "probability", "format": Format(precision=2, scheme=Scheme.fixed)},
            {"name": "Diagonale", "id": "diagonal", "format": Format(precision=2, scheme=Scheme.fixed)},
            {"name": "Hauteur G", "id": "height_left", "format": Format(precision=2, scheme=Scheme.fixed)},
            {"name": "Hauteur D", "id": "height_right", "format": Format(precision=2, scheme=Scheme.fixed)},
            {"name": "Marge Bas", "id": "margin_low", "format": Format(precision=2, scheme=Scheme.fixed)},
            {"name": "Marge Haut", "id": "margin_up", "format": Format(precision=2, scheme=Scheme.fixed)},
            {"name": "Longueur", "id": "length", "format": Format(precision=2, scheme=Scheme.fixed)},
        ],
        page_size=10,
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
            },
            {
                'if': {
                    'filter_query': '{is_fake} eq "true"',
                },
                'backgroundColor': '#ffe6e6',
                'color': '#dc3545'
            },
        ],
        sort_action="native",
        filter_action="native",
    )