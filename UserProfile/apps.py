from django.apps import AppConfig

class UserProfileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'UserProfile'  # Asegúrate de que este sea el nombre correcto de tu aplicación

    def ready(self):
        # Importar las señales para que se conecten
        import UserProfile.signals
