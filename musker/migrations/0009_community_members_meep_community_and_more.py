# Generated by Django 5.1.4 on 2025-08-01 11:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musker', '0008_community'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='joined_communities', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='meep',
            name='community',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='meeps', to='musker.community'),
        ),
        migrations.AlterField(
            model_name='community',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_communities', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='meep',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='meep_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
