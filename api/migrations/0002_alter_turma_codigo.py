# Generated by Django 4.1 on 2022-11-01 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turma',
            name='codigo',
            field=models.CharField(max_length=250, unique=True),
        ),
    ]
