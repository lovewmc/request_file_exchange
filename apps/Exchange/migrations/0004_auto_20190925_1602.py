# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-09-25 16:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Exchange', '0003_domainorder'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='domainorder',
            options={'verbose_name': '域名解析表', 'verbose_name_plural': '域名解析表'},
        ),
        migrations.AlterModelTable(
            name='domainorder',
            table='domain_order',
        ),
    ]
