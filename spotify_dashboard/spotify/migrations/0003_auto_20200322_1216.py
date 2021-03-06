# Generated by Django 2.2.11 on 2020-03-22 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotify', '0002_auto_20200322_1136'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.CharField(max_length=1024)),
                ('scope', models.CharField(max_length=1024)),
                ('refresh_token', models.CharField(max_length=1024)),
                ('expires_in', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('created_at',),
                'get_latest_by': 'created_at',
            },
        ),
        migrations.AlterModelOptions(
            name='code',
            options={'get_latest_by': 'created_at', 'ordering': ('created_at',)},
        ),
    ]
