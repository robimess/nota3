# Generated by Django 5.0.6 on 2024-06-30 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_rename_tasks_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='fecha_termino',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
