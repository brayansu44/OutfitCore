from django.apps import AppConfig


class ProductoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Producto'

    def ready(self):
        import Producto.signals  # Importa las señales
