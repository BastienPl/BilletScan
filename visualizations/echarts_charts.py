import numpy as np

def get_echarts_pie_options(df_results):
    if df_results is None or df_results.empty or 'is_fake' not in df_results.columns:
        return {}
    counts = df_results['is_fake'].value_counts()
    labels = ['Authentiques', 'Contrefaits']
    values = [int(counts.get(False, 0)), int(counts.get(True, 0))]
    colors = ['#4CAF50', '#E74C3C']
    return {
        'title': {
            'text': 'Répartition des billets',
            'left': 'center',
            'top': 10,
            'textStyle': {'fontSize': 20}
        },
        'tooltip': {'trigger': 'item', 'formatter': '{b}: {c} ({d}%)'},
        'legend': {'orient': 'horizontal', 'bottom': 0, 'data': labels},
        'series': [{
            'name': 'Billets',
            'type': 'pie',
            'radius': ['50%', '70%'],
            'avoidLabelOverlap': False,
            'itemStyle': {'borderRadius': 10, 'borderColor': '#fff', 'borderWidth': 2},
            'label': {'show': True, 'position': 'outside', 'fontSize': 16},
            'emphasis': {'label': {'show': True, 'fontSize': 18, 'fontWeight': 'bold'}},
            'labelLine': {'show': True},
            'data': [
                {'value': values[0], 'name': labels[0], 'itemStyle': {'color': colors[0]}},
                {'value': values[1], 'name': labels[1], 'itemStyle': {'color': colors[1]}},
            ]
        }]
    }

def get_echarts_hist_options(df_results):
    if df_results is None or df_results.empty or 'probability' not in df_results.columns:
        return {}
    # Détection de l'échelle de la colonne probability
    max_prob = df_results['probability'].max()
    min_prob = df_results['probability'].min()
    if max_prob > 1.5:  # On suppose 0-100
        bins = np.linspace(0, 100, 21)
        x_labels = [f"{int(b)}" for b in bins[:-1]]
    else:  # On suppose 0-1
        bins = np.linspace(0, 1, 21)
        x_labels = [f"{int(b*100)}" for b in bins[:-1]]
    hist_auth, _ = np.histogram(df_results[df_results['is_fake'] == False]['probability'], bins=bins)
    hist_fake, _ = np.histogram(df_results[df_results['is_fake'] == True]['probability'], bins=bins)
    return {
        'title': {'text': 'Distribution des probabilités', 'left': 'center', 'textStyle': {'fontSize': 20}},
        'tooltip': {'trigger': 'axis'},
        'legend': {'data': ['Authentiques', 'Contrefaits'], 'top': 30},
        'xAxis': {
            'type': 'category',
            'data': x_labels,
            'name': 'Niveau de confiance (%)',
            'nameLocation': 'center',
            'nameGap': 30,
            'axisLabel': {'fontSize': 13}
        },
        'yAxis': {'type': 'value', 'name': 'Nombre', 'nameGap': 20, 'axisLabel': {'fontSize': 13}},
        'series': [
            {
                'name': 'Authentiques',
                'type': 'bar',
                'data': hist_auth.tolist(),
                'itemStyle': {'color': '#4CAF50', 'barBorderRadius': [6, 6, 0, 0]},
                'barWidth': '40%'
            },
            {
                'name': 'Contrefaits',
                'type': 'bar',
                'data': hist_fake.tolist(),
                'itemStyle': {'color': '#E74C3C', 'barBorderRadius': [6, 6, 0, 0]},
                'barWidth': '40%'
            }
        ]
    }

def get_echarts_bar_options(df_data, features):
    if df_data is None or df_data.empty or 'is_fake' not in df_data.columns or not features:
        return {}
    import pandas as pd
    if isinstance(features, str):
        features = [features]
    # Calcul de la moyenne pour chaque feature et chaque groupe
    data = {'Authentiques': [], 'Contrefaits': []}
    for f in features:
        vals_auth = df_data[df_data['is_fake'] == False][f].dropna().values
        vals_fake = df_data[df_data['is_fake'] == True][f].dropna().values
        data['Authentiques'].append(float(np.mean(vals_auth)) if len(vals_auth) else 0)
        data['Contrefaits'].append(float(np.mean(vals_fake)) if len(vals_fake) else 0)
    return {
        'title': {'text': 'Comparaison des moyennes', 'left': 'center', 'textStyle': {'fontSize': 20}},
        'tooltip': {'trigger': 'axis', 'axisPointer': {'type': 'shadow'}},
        'legend': {'data': ['Authentiques', 'Contrefaits'], 'top': 30},
        'xAxis': {
            'type': 'category',
            'data': features,
            'axisLabel': {'fontSize': 13}
        },
        'yAxis': {'type': 'value', 'name': 'Moyenne', 'nameGap': 20, 'axisLabel': {'fontSize': 13}},
        'series': [
            {
                'name': 'Authentiques',
                'type': 'bar',
                'data': data['Authentiques'],
                'itemStyle': {'color': '#4CAF50', 'barBorderRadius': [6, 6, 0, 0]},
                'barWidth': '40%'
            },
            {
                'name': 'Contrefaits',
                'type': 'bar',
                'data': data['Contrefaits'],
                'itemStyle': {'color': '#E74C3C', 'barBorderRadius': [6, 6, 0, 0]},
                'barWidth': '40%'
            }
        ]
    }

def get_echarts_radar_options(df_data, features=None):
    if df_data is None or df_data.empty or 'is_fake' not in df_data.columns:
        return {}
    import numpy as np
    if features is None:
        features = [
            'diagonal', 'height_left', 'height_right', 'margin_low', 'margin_up', 'length'
        ]
    # Calcul des moyennes pour chaque groupe
    means_auth = []
    means_fake = []
    for f in features:
        vals_auth = df_data[df_data['is_fake'] == False][f].dropna().values
        vals_fake = df_data[df_data['is_fake'] == True][f].dropna().values
        means_auth.append(float(np.mean(vals_auth)) if len(vals_auth) else 0)
        means_fake.append(float(np.mean(vals_fake)) if len(vals_fake) else 0)
    # Définition des axes
    indicators = [{
        'name': f,
        'max': float(max(means_auth + means_fake) * 1.2) if (means_auth + means_fake) else 1
    } for f in features]
    return {
        'title': {'text': 'Profil moyen (Radar chart)', 'left': 'center', 'textStyle': {'fontSize': 20}},
        'tooltip': {'trigger': 'item'},
        'legend': {'data': ['Authentiques', 'Contrefaits'], 'top': 30},
        'radar': {
            'indicator': indicators,
            'radius': '65%',
            'splitNumber': 5,
            'axisName': {'fontSize': 13},
        },
        'series': [
            {
                'name': 'Profil moyen',
                'type': 'radar',
                'data': [
                    {
                        'value': means_auth,
                        'name': 'Authentiques',
                        'itemStyle': {'color': '#4CAF50'},
                        'areaStyle': {'opacity': 0.2, 'color': '#4CAF50'}
                    },
                    {
                        'value': means_fake,
                        'name': 'Contrefaits',
                        'itemStyle': {'color': '#E74C3C'},
                        'areaStyle': {'opacity': 0.2, 'color': '#E74C3C'}
                    }
                ]
            }
        ]
    } 