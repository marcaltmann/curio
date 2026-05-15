from datetime import timedelta

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from curio.resources.models import AudioResource

SAMPLES = [
    {
        'title': 'Morning Meditation',
        'duration': timedelta(minutes=10, seconds=32),
        'bitrate': 128000,
        'sample_rate': 44100,
        'channels': 2,
    },
    {
        'title': 'Focus Music',
        'duration': timedelta(minutes=45, seconds=0),
        'bitrate': 192000,
        'sample_rate': 44100,
        'channels': 2,
    },
    {
        'title': 'Evening Wind Down',
        'duration': timedelta(minutes=20, seconds=15),
        'bitrate': 128000,
        'sample_rate': 44100,
        'channels': 1,
    },
]


class Command(BaseCommand):
    help = 'Seed sample AudioResource data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete existing AudioResource records before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            count, _ = AudioResource.objects.all().delete()
            self.stdout.write(f'Deleted {count} existing record(s).')

        for sample in SAMPLES:
            filename = sample['title'].lower().replace(' ', '_') + '.mp3'
            resource = AudioResource(
                title=sample['title'],
                duration=sample['duration'],
                bitrate=sample['bitrate'],
                sample_rate=sample['sample_rate'],
                channels=sample['channels'],
            )
            resource.file.save(filename, ContentFile(b''), save=True)
            self.stdout.write(f'Created: {sample["title"]}')

        self.stdout.write(self.style.SUCCESS('Done.'))
