# Generated by Django 4.2.4 on 2023-09-06 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0006_remove_task_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='next_button_enabled',
            field=models.BooleanField(default=False),
        ),
    ]
