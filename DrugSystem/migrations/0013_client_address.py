# Generated by Django 2.0.2 on 2018-04-19 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DrugSystem', '0012_auto_20180417_0720'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='address',
            field=models.TextField(default='Home'),
            preserve_default=False,
        ),
    ]