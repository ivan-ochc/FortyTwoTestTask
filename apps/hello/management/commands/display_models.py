import django.apps
from django.core.management import BaseCommand
from django.db.models.loading import get_app


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('app', nargs='+', type=str)

    def handle(self, *args, **options):
        app = get_app(options['app'][0])
        for model in django.apps.apps.get_models(app):
            self.stdout.write("Model name: " + str(model._meta.object_name))
            self.stdout.write("Quantity of objects: " +
                              str(model.objects.count()))
            self.stderr.write("error: " + str(model._meta.object_name))
            self.stderr.write("error: " + str(model.objects.count()))
