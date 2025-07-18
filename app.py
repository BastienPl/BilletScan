from dash import Dash, html
import dash_bootstrap_components as dbc

# Imports de tes composants
from components.navbar import create_navbar
from components.header import create_header
from components.features import create_features
from components.upload import create_upload
from components.results import create_results
from components.footer import create_footer

# Imports des callbacks
from callbacks.upload_callbacks import register_upload_callbacks
from callbacks.analysis_callbacks import register_analysis_callbacks

# Config
from config import APP_TITLE, EXTERNAL_STYLESHEETS, get_app_config

# Création de l'application
app = Dash(
    __name__,
    external_stylesheets=EXTERNAL_STYLESHEETS,
    suppress_callback_exceptions=True,
    **get_app_config()
)

# Définition du serveur
server = app.server
app.title = APP_TITLE
app._favicon = 'logo_nav.png'

app.index_string = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    {%metas%}
    <title>{%title%}</title>
    {%favicon%}
    {%css%}
    <style>
        html, body {
            margin: 0;
            padding: 0;
            height: 100%;
            overflow: hidden;
        }
    </style>
</head>
<body>
    <!-- Custom splash screen -->
    <div id="init-loader">
        <div class="spinner">
            <div class="bounce1"></div>
            <div class="bounce2"></div>
            <div class="bounce3"></div>
        </div>
    </div>

    <!-- Zone où Dash injecte l'app -->
    {%app_entry%}

    <footer>
        {%config%}
        {%scripts%}
        {%renderer%}
    </footer>
</body>
</html>
'''

# Layout principal
app.layout = html.Div([
    create_navbar(app),
    create_header(app),
    create_features(),
    create_upload(),
    create_results(),
    create_footer(),
])

# Enregistrement des callbacks
register_upload_callbacks(app)
register_analysis_callbacks(app)

# Démarrage
if __name__ == "__main__":
    app.run(debug=True)