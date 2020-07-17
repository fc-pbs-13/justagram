# Generated by Django 3.0.7 on 2020-07-17 03:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('relations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='follow',
            name='from_follow_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_follow_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='follow',
            name='to_follow_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_follow_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together={('from_follow_user', 'to_follow_user')},
        ),
    ]
