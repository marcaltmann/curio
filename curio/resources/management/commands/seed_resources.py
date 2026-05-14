import io

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from curio.resources.models import AudioResource

SAMPLES = [
    "Morning Meditation",
    "Focus Music",
    "Evening Wind Down",
]


class Command(BaseCommand):
    help = "Seed sample AudioResource data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete existing AudioResource records before seeding",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            count, _ = AudioResource.objects.all().delete()
            self.stdout.write(f"Deleted {count} existing record(s).")

        for title in SAMPLES:
            filename = title.lower().replace(" ", "_") + ".mp3"
            resource = AudioResource(title=title)
            resource.file.save(filename, ContentFile(b""), save=True)
            self.stdout.write(f"Created: {title}")

        self.stdout.write(self.style.SUCCESS("Done."))
