from django.apps import AppConfig

class DemoAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'demo_app'

    def ready(self):
        import demo_app.signals  # Import signals to register them