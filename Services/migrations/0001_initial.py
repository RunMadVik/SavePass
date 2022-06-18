# Generated by Django 4.0.5 on 2022-06-18 07:18

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=200, unique=True, verbose_name='Service Name')),
                ('service_login_url', models.URLField(unique=True, verbose_name='Service Login URL')),
                ('service_reset_password_url', models.URLField(unique=True, verbose_name='Service Password Reset URL')),
            ],
        ),
    ]
