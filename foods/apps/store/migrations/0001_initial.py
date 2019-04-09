# Generated by Django 2.0.9 on 2019-04-04 09:45

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('material', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(db_index=True, max_length=50, unique=True, verbose_name='项目名称')),
                ('address', models.CharField(blank=True, max_length=200, null=True, verbose_name='项目地址')),
                ('scope', models.FloatField(blank=True, default=0, null=True, verbose_name='服务范围(km)')),
                ('point', models.CharField(blank=True, max_length=30, null=True, verbose_name='坐标')),
                ('enable', models.BooleanField(default=True, verbose_name='是否启用')),
                ('fee', models.FloatField(default=0, verbose_name='配送费')),
                ('minQty', models.FloatField(default=0, verbose_name='超过后免配送费')),
                ('preferential', models.FloatField(default=0, verbose_name='项目优惠(元)')),
            ],
            options={
                'verbose_name': '项目资料',
                'verbose_name_plural': '项目资料',
            },
        ),
        migrations.CreateModel(
            name='StoreMats',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('enable_from', models.DateField(verbose_name='启用时间')),
                ('enable_to', models.DateField(blank=True, null=True, verbose_name='停用时间')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('material', models.ManyToManyField(db_constraint=False, null=True, related_name='project_material', to='material.Material', verbose_name='当前上架商品')),
                ('store', models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='store_mats', to='store.Store', verbose_name='项目')),
            ],
            options={
                'verbose_name': '项目上架商品',
                'verbose_name_plural': '项目上架商品',
            },
        ),
    ]