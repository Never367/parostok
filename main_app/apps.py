from django.apps import AppConfig
from elasticsearch_dsl import connections
from django.conf import settings


class MainAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main_app'
    verbose_name = 'Товари'

    def ready(self):
        import main_app.signals
        try:
            connections.create_connection(
                hosts=[{'host': settings.ES_HOST, 'port': settings.ES_PORT}]
            )
        except Exception as e:
            print(e)
