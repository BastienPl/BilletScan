"""
Module contenant les callbacks de l'application BilletScan.
"""

from .upload_callbacks import register_upload_callbacks
from .analysis_callbacks import register_analysis_callbacks

__all__ = [
    'register_upload_callbacks',
    'register_analysis_callbacks'
]