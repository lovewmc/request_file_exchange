# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-10-14 10:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DomainOrder',
            fields=[
                ('domain_name', models.CharField(max_length=30, primary_key=True, serialize=False, verbose_name='域名')),
                ('ip', models.CharField(blank=True, max_length=30, null=True, verbose_name='ip')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('modify_time', models.DateTimeField(auto_now=True, null=True, verbose_name='修改时间')),
                ('kind', models.CharField(blank=True, max_length=20, null=True, verbose_name='网络类型')),
            ],
            options={
                'verbose_name': '域名解析表',
                'verbose_name_plural': '域名解析表',
                'db_table': 'domain_order',
            },
        ),
        migrations.CreateModel(
            name='RequestHistoryOrder',
            fields=[
                ('unique_code', models.CharField(max_length=30, primary_key=True, serialize=False, verbose_name='唯一标识')),
                ('identity_code', models.CharField(blank=True, max_length=30, null=True, verbose_name='请求id')),
                ('request_data', models.TextField(blank=True, null=True, verbose_name='请求数据')),
                ('response_data', models.TextField(blank=True, null=True, verbose_name='返回数据')),
                ('received_time', models.DateTimeField(blank=True, null=True, verbose_name='接收请求时间')),
                ('create_file_time', models.DateTimeField(blank=True, null=True, verbose_name='生成文件时间')),
                ('read_file_time', models.DateTimeField(blank=True, null=True, verbose_name='读取文件时间')),
                ('return_time', models.DateTimeField(blank=True, null=True, verbose_name='请求成功时间')),
                ('write_status', models.CharField(choices=[('0', '初始状态'), ('1', '接收请求'), ('2', '生成文件')], default='0', max_length=10, verbose_name='写状态')),
                ('read_status', models.CharField(choices=[('0', '初始状态'), ('1', '读取文件'), ('2', '请求成功')], default='0', max_length=10, verbose_name='读状态')),
                ('finish_tag', models.BooleanField(default=False, verbose_name='完成标记')),
                ('request_flag', models.CharField(choices=[('0', '初始状态'), ('1', '请求'), ('2', '返回')], default='0', max_length=10, verbose_name='请求标志')),
            ],
            options={
                'verbose_name': '请求记录表',
                'verbose_name_plural': '请求记录表',
                'db_table': 'request_order',
            },
        ),
    ]
