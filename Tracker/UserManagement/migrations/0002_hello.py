# Generated by Django 3.2.6 on 2022-05-08 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserManagement', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hello',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
    ]
