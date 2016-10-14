from django.core.management import BaseCommand
import languages.console as lc
import gistsapi.console as gc

class Command(BaseCommand):
    @staticmethod
    def populate():
        lc.populate()
        gc.populate()

    def handle(self, *args, **options):
        self.populate()

