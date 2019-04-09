# Generated by Django 2.0.9 on 2019-04-03 19:00

import DjangoUeditor.models
from django.db import migrations, models
import easy_thumbnails.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('SKU', models.CharField(db_index=True, max_length=50, verbose_name='SKU')),
                ('name', models.CharField(db_index=True, max_length=150, verbose_name='菜品名称')),
                ('price', models.FloatField(default=0, verbose_name='单价')),
                ('description', DjangoUeditor.models.UEditorField(default='', verbose_name='描述')),
                ('image', easy_thumbnails.fields.ThumbnailerImageField(blank=True, null=True, upload_to='images/%Y/%m', verbose_name='图片')),
                ('banner', models.BooleanField(default=False, verbose_name='轮播广告')),
                ('remark', DjangoUeditor.models.UEditorField(default='', verbose_name='备注')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='修改时间')),
            ],
            options={
                'verbose_name': '堂食菜品',
                'verbose_name_plural': '堂食菜品',
            },
        ),
        migrations.CreateModel(
            name='MatType',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(db_index=True, max_length=50, unique=True, verbose_name='分类编码')),
                ('name', models.CharField(db_index=True, max_length=150, verbose_name='分类名称')),
                ('remark', models.CharField(blank=True, max_length=150, null=True, verbose_name='备注')),
                ('enable', models.BooleanField(default=True, verbose_name='是否启用')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='修改时间')),
            ],
            options={
                'verbose_name': '菜品类别',
                'verbose_name_plural': '菜品类别',
            },
        ),
    ]
