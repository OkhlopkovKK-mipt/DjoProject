"""
App configuration for the catalog application.
"""

from django.apps import AppConfig


class CatalogConfig(AppConfig):
    """App configuration for the catalog application."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalog'
