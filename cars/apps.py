from django.apps import AppConfig


class CarConfig(AppConfig):
    verbose_name = 'Автомобили'
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cars'
