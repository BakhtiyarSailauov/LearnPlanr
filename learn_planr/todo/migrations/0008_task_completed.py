# Generated by Django 4.2.4 on 2023-09-09 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0007_chapter_next_button_enabled'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
