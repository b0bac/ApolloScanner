# Generated by Django 4.0.1 on 2022-03-10 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Configuration', '0005_services_ip_address_alter_services_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='services',
            name='state',
            field=models.BooleanField(db_column='state', default=False, verbose_name='服务开启'),
        ),
    ]
