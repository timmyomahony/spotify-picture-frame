# Generated by Django 3.1 on 2020-11-02 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotify', '0009_auto_20201102_2328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='id',
            field=models.CharField(max_length=30, primary_key=True, serialize=False),
        ),
    ]
