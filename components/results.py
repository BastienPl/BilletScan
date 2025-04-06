"""
Composant pour afficher les résultats de l'analyse des billets.
"""

import dash_bootstrap_components as dbc
from dash import html, dcc

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
                          fig_distr, fig_radar, fig_boxplot, fig_scatter, fig_3d, 
                          df_results_with_features, initial_features):
    """
    Génère le contenu à afficher dans la section des résultats après analyse.
    
    Args:
        total_banknotes (int): Nombre total de billets analysés.
        fake_banknotes (int): Nombre de faux billets détectés.
        fake_percentage (float): Pourcentage de faux billets.
        filename (str): Nom du fichier analysé.
        fig_distr (plotly.graph_objects.Figure): Figure de distribution des probabilités.
        fig_radar (plotly.graph_objects.Figure): Figure du graphique radar.
        fig_boxplot (plotly.graph_objects.Figure): Figure des boîtes à moustaches.
        fig_scatter (plotly.graph_objects.Figure): Figure de la matrice de dispersion.
        fig_3d (plotly.graph_objects.Figure): Figure du graphique 3D.
        df_results_with_features (pandas.DataFrame): DataFrame contenant les résultats avec caractéristiques.
        initial_features (list): Liste initiale des caractéristiques pour la matrice de dispersion.
        
    Returns:
        list: Liste des composants à afficher.
    """
    return [
        dbc.Row(
            [
                dbc.Col(
                    html.H2("Résultats de l'analyse", className="mb-4 text-primary"),
                    width=12,
                ),
            ],
            className="mb-4",
        ),
        
        # Cartes de statistiques
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H3(
                                        total_banknotes,
                                        className="card-title text-center display-4"
                                    ),
                                    html.P(
                                        "Billets analysés",
                                        className="card-text text-center text-muted"
                                    ),
                                ]
                            ),
                            dbc.CardFooter(
                                html.Small(
                                    f"Fichier : {filename}",
                                    className="text-muted"
                                )
                            ),
                        ],
                        className="text-center h-100 shadow-sm"
                    ),
                    md=4,
                    className="mb-4",
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H3(
                                        fake_banknotes,
                                        className="card-title text-center display-4 text-danger" 
                                            if fake_banknotes > 0 else 
                                        "card-title text-center display-4 text-success"
                                    ),
                                    html.P(
                                        "Faux billets détectés",
                                        className="card-text text-center text-muted"
                                    ),
                                ]
                            ),
                            dbc.CardFooter(
                                html.Small(
                                    [
                                        html.I(
                                            className="fas fa-exclamation-triangle me-1 text-danger" 
                                                if fake_banknotes > 0 else 
                                            "fas fa-check-circle me-1 text-success"
                                        ),
                                        f"{fake_percentage:.1f}% des billets analysés"
                                    ],
                                    className="text-muted"
                                )
                            ),
                        ],
                        className="text-center h-100 shadow-sm",
                        color="danger" if fake_banknotes > 0 else "success",
                        outline=True
                    ),
                    md=4,
                    className="mb-4",
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H3(
                                        f"{df_results_with_features['probability'].mean():.1f}%",
                                        className="card-title text-center display-4"
                                    ),
                                    html.P(
                                        "Niveau de confiance moyen",
                                        className="card-text text-center text-muted"
                                    ),
                                ]
                            ),
                            dbc.CardFooter(
                                html.Small(
                                    [
                                        html.I(className="fas fa-chart-line me-1"),
                                        f"Min: {df_results_with_features['probability'].min():.1f}% | Max: {df_results_with_features['probability'].max():.1f}%"
                                    ],
                                    className="text-muted"
                                )
                            ),
                        ],
                        className="text-center h-100 shadow-sm"
                    ),
                    md=4,
                    className="mb-4",
                ),
            ],
            className="mb-4",
        ),
        
        # Onglets pour les différentes visualisations
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Tabs(
                            [
                                dbc.Tab(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dcc.Graph(
                                                        figure=fig_distr,
                                                        config={'displayModeBar': False}
                                                    ),
                                                    md=6,
                                                ),
                                                dbc.Col(
                                                    dcc.Graph(
                                                        figure=fig_radar,
                                                        config={'displayModeBar': False}
                                                    ),
                                                    md=6,
                                                ),
                                            ],
                                            className="mb-4",
                                        ),
                                        dbc.Card(
                                            [
                                                dbc.CardHeader("Analyse détaillée"),
                                                dbc.CardBody(
                                                    dcc.Graph(
                                                        figure=fig_boxplot,
                                                        config={'displayModeBar': True}
                                                    ),
                                                ),
                                            ],
                                            className="shadow-sm",
                                        ),
                                    ],
                                    label="Aperçu général",
                                    tab_id="tab-general",
                                ),
                                dbc.Tab(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        dbc.Card(
                                                            [
                                                                dbc.CardHeader("Caractéristiques à comparer"),
                                                                dbc.CardBody(
                                                                    [
                                                                        dbc.Label("Sélectionnez au moins 2 caractéristiques:"),
                                                                        dcc.Checklist(
                                                                            id="feature-checklist",
                                                                            options=[
                                                                                {'label': ' Diagonale', 'value': 'diagonal'},
                                                                                {'label': ' Hauteur gauche', 'value': 'height_left'},
                                                                                {'label': ' Hauteur droite', 'value': 'height_right'},
                                                                                {'label': ' Marge basse', 'value': 'margin_low'},
                                                                                {'label': ' Marge haute', 'value': 'margin_up'},
                                                                                {'label': ' Longueur', 'value': 'length'},
                                                                            ],
                                                                            value=initial_features,
                                                                            className="my-2",
                                                                            inputStyle={"marginRight": "5px"}
                                                                        ),
                                                                    ]
                                                                ),
                                                            ],
                                                            className="shadow-sm mb-4",
                                                        ),
                                                        dbc.Card(
                                                            [
                                                                dbc.CardHeader("Tableau de données"),
                                                                dbc.CardBody(
                                                                    [
                                                                        create_results_table(df_results_with_features),
                                                                        html.Div(
                                                                            [
                                                                                dbc.Button(
                                                                                    [
                                                                                        html.I(className="fas fa-download me-2"),
                                                                                        "Télécharger les résultats (CSV)"
                                                                                    ],
                                                                                    id="btn-download-csv",
                                                                                    color="primary",
                                                                                    outline=True,
                                                                                    size="sm",
                                                                                    className="mt-3",
                                                                                ),
                                                                            ],
                                                                            className="d-flex justify-content-end",
                                                                        ),
                                                                    ]
                                                                ),
                                                            ],
                                                            className="shadow-sm",
                                                        ),
                                                    ],
                                                    md=5,
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Card(
                                                            [
                                                                dbc.CardHeader("Matrice de corrélation des caractéristiques"),
                                                                dbc.CardBody(
                                                                    dcc.Graph(
                                                                        id="scatter-matrix",
                                                                        figure=fig_scatter,
                                                                        config={'displayModeBar': True}
                                                                    ),
                                                                ),
                                                            ],
                                                            className="shadow-sm h-100",
                                                        ),
                                                    ],
                                                    md=7,
                                                ),
                                            ],
                                        ),
                                    ],
                                    label="Analyse détaillée",
                                    tab_id="tab-details",
                                ),
                                dbc.Tab(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        dbc.Card(
                                                            [
                                                                dbc.CardHeader("Paramètres de visualisation 3D"),
                                                                dbc.CardBody(
                                                                    [
                                                                        dbc.Row(
                                                                            [
                                                                                dbc.Col(
                                                                                    [
                                                                                        dbc.Label("Dimension X:"),
                                                                                        dcc.Dropdown(
                                                                                            id="dim-x-dropdown",
                                                                                            options=[
                                                                                                {'label': 'Diagonale', 'value': 'diagonal'},
                                                                                                {'label': 'Hauteur gauche', 'value': 'height_left'},
                                                                                                {'label': 'Hauteur droite', 'value': 'height_right'},
                                                                                                {'label': 'Marge basse', 'value': 'margin_low'},
                                                                                                {'label': 'Marge haute', 'value': 'margin_up'},
                                                                                                {'label': 'Longueur', 'value': 'length'},
                                                                                            ],
                                                                                            value="length",
                                                                                        ),
                                                                                    ],
                                                                                    md=6,
                                                                                ),
                                                                                dbc.Col(
                                                                                    [
                                                                                        dbc.Label("Dimension Y:"),
                                                                                        dcc.Dropdown(
                                                                                            id="dim-y-dropdown",
                                                                                            options=[
                                                                                                {'label': 'Diagonale', 'value': 'diagonal'},
                                                                                                {'label': 'Hauteur gauche', 'value': 'height_left'},
                                                                                                {'label': 'Hauteur droite', 'value': 'height_right'},
                                                                                                {'label': 'Marge basse', 'value': 'margin_low'},
                                                                                                {'label': 'Marge haute', 'value': 'margin_up'},
                                                                                                {'label': 'Longueur', 'value': 'length'},
                                                                                            ],
                                                                                            value="diagonal",
                                                                                        ),
                                                                                    ],
                                                                                    md=6,
                                                                                ),
                                                                            ],
                                                                            className="mb-3",
                                                                        ),
                                                                        html.P(
                                                                            [
                                                                                html.I(className="fas fa-info-circle me-2 text-info"),
                                                                                "Utilisez la souris pour faire pivoter le graphique et explorer les relations entre les dimensions et la probabilité."
                                                                            ],
                                                                            className="small text-muted mt-2",
                                                                        ),
                                                                    ]
                                                                ),
                                                            ],
                                                            className="shadow-sm mb-4",
                                                        ),
                                                        dbc.Card(
                                                            [
                                                                dbc.CardHeader("Information"),
                                                                dbc.CardBody(
                                                                    [
                                                                        html.H5("Comment interpréter ce graphique"),
                                                                        html.P(
                                                                            "Ce graphique 3D montre la relation entre deux dimensions des billets (X et Y) et leur niveau de confiance (Z)."
                                                                        ),
                                                                        html.P(
                                                                            [
                                                                                "Les points ",
                                                                                html.Span("verts", className="text-success fw-bold"),
                                                                                " représentent les billets authentiques, tandis que les points ",
                                                                                html.Span("rouges", className="text-danger fw-bold"),
                                                                                " représentent les billets contrefaits.",
                                                                            ]
                                                                        ),
                                                                        html.P(
                                                                            "La hauteur (axe Z) indique le niveau de confiance de la prédiction."
                                                                        ),
                                                                    ]
                                                                ),
                                                            ],
                                                            className="shadow-sm",
                                                        ),
                                                    ],
                                                    md=4,
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Card(
                                                            [
                                                                dbc.CardHeader("Visualisation 3D des résultats"),
                                                                dbc.CardBody(
                                                                    dcc.Graph(
                                                                        id="3d-scatter",
                                                                        figure=fig_3d,
                                                                        config={'displayModeBar': True}
                                                                    ),
                                                                ),
                                                            ],
                                                            className="shadow-sm h-100",
                                                        ),
                                                    ],
                                                    md=8,
                                                ),
                                            ],
                                        ),
                                    ],
                                    label="Visualisation 3D",
                                    tab_id="tab-3d",
                                ),
                            ],
                            id="tabs",
                            active_tab="tab-general",
                        ),
                    ],
                    width=12,
                ),
            ],
            className="mb-4",
        ),
        
        # Footer avec statistiques et boutons d'action
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        html.P(
                                                            [
                                                                html.I(className="fas fa-check-circle me-2 text-success"),
                                                                f"Billets authentiques: {(total_banknotes - fake_banknotes)} ({100 - fake_percentage:.1f}%)"
                                                            ],
                                                            className="mb-0 text-success fw-bold"
                                                        ),
                                                    ],
                                                    md=4,
                                                ),
                                                dbc.Col(
                                                    [
                                                        html.P(
                                                            [
                                                                html.I(className="fas fa-times-circle me-2 text-danger"),
                                                                f"Billets contrefaits: {fake_banknotes} ({fake_percentage:.1f}%)"
                                                            ],
                                                            className="mb-0 text-danger fw-bold"
                                                        ),
                                                    ],
                                                    md=4,
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Button(
                                                            [
                                                                html.I(className="fas fa-redo-alt me-2"),
                                                                "Nouvelle analyse"
                                                            ],
                                                            href="#upload-section",
                                                            color="primary",
                                                            className="float-end",
                                                        ),
                                                    ],
                                                    md=4,
                                                ),
                                            ],
                                        ),
                                    ]
                                ),
                            ],
                            className="shadow-sm"
                        ),
                    ],
                    width=12,
                ),
            ],
        ),
        
        # Composant de téléchargement
        dcc.Download(id="download-results"),
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