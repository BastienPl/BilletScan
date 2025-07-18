"""
Module contenant les fonctionnalités liées aux modèles de ML de l'application BilletScan.
"""

from .model_loader import load_model, predict, clf

__all__ = [
    'load_model',
    'predict',
    'clf'
]
