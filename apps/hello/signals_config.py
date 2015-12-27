from django.apps import AppConfig


class SignalsConfig(AppConfig):
    name = 'apps.hello'
    verbose_name = 'Hello Application'

    def ready(self):
        import apps.hello.signals
