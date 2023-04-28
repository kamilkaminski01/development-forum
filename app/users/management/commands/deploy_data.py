from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = "Initialize deployment data"

    def handle(self, **options):
        call_command("loaddata", "users/fixtures/deploy_data.json")
