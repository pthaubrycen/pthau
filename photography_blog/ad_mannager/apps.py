from django.apps import AppConfig


class AdMannagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ad_mannager'
    
    def ready(self):
        import ad_mannager.signals
