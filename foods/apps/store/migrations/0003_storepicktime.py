# Generated by Django 2.0.9 on 2019-04-08 09:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_store_head'),
    ]

    operations = [
        migrations.CreateModel(
            name='StorePickTime',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('start_time', models.TimeField(verbose_name='开始时间')),
                ('end_time', models.TimeField(verbose_name='结束时间')),
                ('store', models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='store_pickup_times', to='store.Store', verbose_name='项目')),
            ],
            options={
                'verbose_name': '项目取件时段',
                'verbose_name_plural': '项目取件时段',
            },
        ),
    ]