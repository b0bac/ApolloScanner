# Generated by Django 4.0.1 on 2022-03-08 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.AutoField(db_column='id', primary_key=True, serialize=False, verbose_name='序号')),
                ('name', models.CharField(choices=[('1', 'VT接口'), ('2', '钉钉接口'), ('3', 'Github接口'), ('4', '钟馗接口'), ('5', '佛法接口'), ('6', '线程数'), ('7', '系统地址'), ('8', '系统域名'), ('9', '常用端口'), ('10', '关键端口')], max_length=2, unique=True, verbose_name='配置名称')),
                ('user', models.CharField(blank=True, db_column='user', max_length=128, null=True, verbose_name='用户名')),
                ('value', models.CharField(blank=True, db_column='value', max_length=512, null=True, verbose_name='Token令牌')),
                ('port', models.TextField(blank=True, db_column='port', null=True, verbose_name='端口列表')),
                ('ipaddress', models.GenericIPAddressField(blank=True, db_column='ipaddress', default='127.0.0.1', null=True, verbose_name='系统地址')),
                ('domain', models.CharField(blank=True, db_column='domain', default='apollo.local', max_length=256, null=True, verbose_name='系统域名')),
                ('count', models.IntegerField(blank=True, db_column='count', default=10, null=True, verbose_name='配置值')),
                ('timestamp', models.DateField(db_column='deadline', verbose_name='创建日期')),
            ],
            options={
                'verbose_name': '配置信息',
                'verbose_name_plural': '配置信息',
            },
        ),
    ]
