# Generated by Django 4.0.5 on 2022-08-19 04:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0005_auto_20220424_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=15, null=True)),
                ('task', models.CharField(max_length=255, null=True)),
                ('address', models.CharField(max_length=255, null=True)),
                ('birthday', models.DateField(null=True)),
                ('avatar', models.ImageField(default='default.png', upload_to='profile_images')),
                ('bio', models.TextField(null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('thumbnail', models.FileField(upload_to='thumbnail image')),
                ('slug', models.SlugField(unique=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateField(auto_now=True)),
                ('isDelete', models.BooleanField(default=False)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ad_mannager.category')),
                ('status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ad_mannager.status')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
