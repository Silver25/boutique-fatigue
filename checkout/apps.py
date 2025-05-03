from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'checkout'

    # overriding the ready method and importing our signals module.
    def ready(self):
        import checkout.signals
