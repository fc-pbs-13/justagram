# Generated by Django 3.0.7 on 2020-07-22 05:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stories', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stories', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='checkshow',
            name='show_story',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='show_stories', to='stories.Story'),
        ),
        migrations.AddField(
            model_name='checkshow',
            name='show_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='show_users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='checkshow',
            unique_together={('show_story', 'show_user')},
        ),
    ]
