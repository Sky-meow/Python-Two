# Generated by Django 2.0.9 on 2019-04-03 19:00

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SmsLog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('key', models.CharField(max_length=20, verbose_name='短信提醒事件')),
                ('content', models.CharField(max_length=280, verbose_name='短信模板内容')),
                ('sendTime', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('status', models.CharField(blank=True, max_length=25, null=True, verbose_name='状态')),
                ('reason', models.CharField(blank=True, max_length=100, null=True, verbose_name='记录')),
            ],
            options={
                'verbose_name': '短信日志',
                'verbose_name_plural': '短信日志',
            },
        ),
        migrations.CreateModel(
            name='SmsTemplate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=25, null=True, verbose_name='模板名称')),
                ('templateId', models.CharField(max_length=50, verbose_name='短信服务模板ID')),
                ('key', models.CharField(blank=True, choices=[('neworder', '新订单提醒'), ('pickup', '派送中提醒'), ('bindphone_captch', '绑定手机验证'), ('chphone_captch', '更换手机验证')], db_index=True, max_length=20, null=True, verbose_name='短信提醒事件')),
                ('content', models.TextField(max_length=280, verbose_name='短信模板内容')),
                ('enable', models.BooleanField(default=True, verbose_name='启用')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='修改时间')),
            ],
            options={
                'verbose_name': '短信模板',
                'verbose_name_plural': '短信模板',
            },
        ),
    ]
