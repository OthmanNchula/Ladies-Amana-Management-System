from django.apps import AppConfig


class AdminappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'adminApp'
    
    def ready(self):
        import adminApp.signals
