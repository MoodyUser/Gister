from django.core.management import BaseCommand
import languages.console as lc
import gistsapi.console as gc


class Command(BaseCommand):
    @staticmethod
    def update():
        gc.update()

    def handle(self, *args, **options):
        self.update()
