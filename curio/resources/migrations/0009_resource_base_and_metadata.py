import django.db.models.deletion
from django.db import migrations, models


def create_resource_records(apps, schema_editor):
    db = schema_editor.connection.alias
    Resource = apps.get_model('resources', 'Resource')
    for model_name in ('AudioResource', 'ImageResource', 'VideoResource'):
        Model = apps.get_model('resources', model_name)
        for obj in Model.objects.using(db).all():
            resource = Resource.objects.using(db).create(
                title=obj.title,
                file_size=obj.file_size,
            )
            obj.resource_ptr_id = resource.pk
            obj.save(using=db, update_fields=['resource_ptr_id'])


_SWAP_SQL = """
    ALTER TABLE {table} DROP CONSTRAINT {table}_pkey CASCADE;
    ALTER TABLE {table} ALTER COLUMN resource_ptr_id SET NOT NULL;
    ALTER TABLE {table} ADD PRIMARY KEY (resource_ptr_id);
    ALTER TABLE {table} DROP COLUMN id;
    ALTER TABLE {table} DROP COLUMN title;
    ALTER TABLE {table} DROP COLUMN file_size;
    ALTER TABLE {table} DROP COLUMN created_at;
    ALTER TABLE {table} DROP COLUMN updated_at;
"""

_AUDIO_FIELDS = [
    (
        'resource_ptr',
        models.OneToOneField(
            auto_created=True,
            on_delete=django.db.models.deletion.CASCADE,
            parent_link=True,
            primary_key=True,
            serialize=False,
            to='resources.resource',
        ),
    ),
    ('file', models.FileField(upload_to='audio/', verbose_name='file')),
    ('duration', models.DurationField(blank=True, null=True, verbose_name='duration')),
    (
        'bitrate',
        models.PositiveIntegerField(blank=True, null=True, verbose_name='bitrate'),
    ),
    (
        'sample_rate',
        models.PositiveIntegerField(blank=True, null=True, verbose_name='sample rate'),
    ),
    (
        'channels',
        models.PositiveSmallIntegerField(
            blank=True, null=True, verbose_name='channels'
        ),
    ),
]

_IMAGE_FIELDS = [
    (
        'resource_ptr',
        models.OneToOneField(
            auto_created=True,
            on_delete=django.db.models.deletion.CASCADE,
            parent_link=True,
            primary_key=True,
            serialize=False,
            to='resources.resource',
        ),
    ),
    ('file', models.ImageField(upload_to='images/', verbose_name='file')),
    ('width', models.PositiveIntegerField(blank=True, null=True, verbose_name='width')),
    (
        'height',
        models.PositiveIntegerField(blank=True, null=True, verbose_name='height'),
    ),
    (
        'format',
        models.CharField(blank=True, max_length=32, null=True, verbose_name='format'),
    ),
    (
        'color_mode',
        models.CharField(
            blank=True, max_length=16, null=True, verbose_name='color mode'
        ),
    ),
    (
        'icc_profile',
        models.CharField(
            blank=True, max_length=255, null=True, verbose_name='ICC profile'
        ),
    ),
    ('taken_at', models.DateTimeField(blank=True, null=True, verbose_name='taken at')),
    (
        'camera_make',
        models.CharField(
            blank=True, max_length=64, null=True, verbose_name='camera make'
        ),
    ),
    (
        'camera_model',
        models.CharField(
            blank=True, max_length=64, null=True, verbose_name='camera model'
        ),
    ),
]

_VIDEO_FIELDS = [
    (
        'resource_ptr',
        models.OneToOneField(
            auto_created=True,
            on_delete=django.db.models.deletion.CASCADE,
            parent_link=True,
            primary_key=True,
            serialize=False,
            to='resources.resource',
        ),
    ),
    ('file', models.FileField(upload_to='videos/', verbose_name='file')),
    (
        'poster',
        models.ImageField(
            blank=True, null=True, upload_to='video_posters/', verbose_name='poster'
        ),
    ),
    ('duration', models.DurationField(blank=True, null=True, verbose_name='duration')),
    ('width', models.PositiveIntegerField(blank=True, null=True, verbose_name='width')),
    (
        'height',
        models.PositiveIntegerField(blank=True, null=True, verbose_name='height'),
    ),
    (
        'bitrate',
        models.PositiveIntegerField(blank=True, null=True, verbose_name='bitrate'),
    ),
    (
        'video_codec',
        models.CharField(
            blank=True, max_length=64, null=True, verbose_name='video codec'
        ),
    ),
    (
        'frame_rate_num',
        models.PositiveIntegerField(
            blank=True, null=True, verbose_name='frame rate numerator'
        ),
    ),
    (
        'frame_rate_den',
        models.PositiveIntegerField(
            blank=True, null=True, verbose_name='frame rate denominator'
        ),
    ),
    (
        'audio_codec',
        models.CharField(
            blank=True, max_length=64, null=True, verbose_name='audio codec'
        ),
    ),
]


class Migration(migrations.Migration):
    dependencies = [
        ('resources', '0008_videoresource'),
    ]

    operations = [
        # ── Phase 1: create the Resource parent table ──────────────────────
        migrations.CreateModel(
            name='Resource',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                (
                    'file_size',
                    models.PositiveIntegerField(default=0, verbose_name='file size'),
                ),
                (
                    'created_at',
                    models.DateTimeField(auto_now_add=True, verbose_name='created at'),
                ),
                (
                    'updated_at',
                    models.DateTimeField(auto_now=True, verbose_name='updated at'),
                ),
            ],
            options={
                'verbose_name': 'resource',
                'verbose_name_plural': 'resources',
            },
        ),
        # ── Phase 2: add nullable resource_ptr to each child ───────────────
        migrations.AddField(
            model_name='audioresource',
            name='resource_ptr',
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                parent_link=True,
                to='resources.resource',
            ),
        ),
        migrations.AddField(
            model_name='imageresource',
            name='resource_ptr',
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                parent_link=True,
                to='resources.resource',
            ),
        ),
        migrations.AddField(
            model_name='videoresource',
            name='resource_ptr',
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                parent_link=True,
                to='resources.resource',
            ),
        ),
        # ── Phase 3: populate Resource rows from existing child data ────────
        migrations.RunPython(create_resource_records, migrations.RunPython.noop),
        # ── Phase 4: swap PKs and drop common columns ───────────────────────
        # database_operations execute real SQL; state_operations update Django's
        # internal model representation without touching the DB a second time.
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql=_SWAP_SQL.format(table='resources_audioresource'),
                    reverse_sql=migrations.RunSQL.noop,
                ),
                migrations.RunSQL(
                    sql=_SWAP_SQL.format(table='resources_imageresource'),
                    reverse_sql=migrations.RunSQL.noop,
                ),
                migrations.RunSQL(
                    sql=_SWAP_SQL.format(table='resources_videoresource'),
                    reverse_sql=migrations.RunSQL.noop,
                ),
            ],
            state_operations=[
                migrations.DeleteModel('AudioResource'),
                migrations.CreateModel(
                    name='AudioResource',
                    fields=_AUDIO_FIELDS,
                    options={
                        'verbose_name': 'audio resource',
                        'verbose_name_plural': 'audio resources',
                    },
                    bases=('resources.resource',),
                ),
                migrations.DeleteModel('ImageResource'),
                migrations.CreateModel(
                    name='ImageResource',
                    fields=_IMAGE_FIELDS,
                    options={
                        'verbose_name': 'image resource',
                        'verbose_name_plural': 'image resources',
                    },
                    bases=('resources.resource',),
                ),
                migrations.DeleteModel('VideoResource'),
                migrations.CreateModel(
                    name='VideoResource',
                    fields=_VIDEO_FIELDS,
                    options={
                        'verbose_name': 'video resource',
                        'verbose_name_plural': 'video resources',
                    },
                    bases=('resources.resource',),
                ),
            ],
        ),
        # ── Phase 5: create Metadata ────────────────────────────────────────
        migrations.CreateModel(
            name='Metadata',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'resource',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='metadata',
                        to='resources.resource',
                        verbose_name='resource',
                    ),
                ),
                (
                    'type',
                    models.CharField(
                        choices=[
                            ('exif', 'EXIF'),
                            ('dc', 'Dublin Core'),
                            ('custom', 'Custom'),
                        ],
                        max_length=16,
                        verbose_name='type',
                    ),
                ),
                ('data', models.JSONField(verbose_name='data')),
                (
                    'created_at',
                    models.DateTimeField(auto_now_add=True, verbose_name='created at'),
                ),
                (
                    'updated_at',
                    models.DateTimeField(auto_now=True, verbose_name='updated at'),
                ),
            ],
            options={
                'verbose_name': 'metadata',
                'verbose_name_plural': 'metadata',
            },
        ),
    ]
