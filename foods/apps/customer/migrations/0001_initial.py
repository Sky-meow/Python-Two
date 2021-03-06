# Generated by Django 2.0.9 on 2019-04-03 19:00

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('contact', models.CharField(max_length=30, null=True, verbose_name='联系人')),
                ('telnumber', models.CharField(max_length=30, null=True, verbose_name='联系电话')),
                ('address', models.CharField(max_length=150, null=True, verbose_name='送餐地址')),
                ('housenum', models.CharField(max_length=100, null=True, verbose_name='门牌号')),
                ('point', models.CharField(max_length=30, null=True, verbose_name='坐标')),
                ('is_default', models.BooleanField(default=False, verbose_name='是否默认')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '送餐地址',
                'verbose_name_plural': '送餐地址',
            },
        ),
        migrations.CreateModel(
            name='BuesinessApply',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('company', models.CharField(blank=True, db_index=True, max_length=100, verbose_name='公司名称')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='申请时间')),
                ('is_pass', models.NullBooleanField(default=None, verbose_name='是否通过')),
                ('settlement_cycle', models.IntegerField(default=0, verbose_name='结算天数')),
                ('minprice', models.FloatField(default=0, verbose_name='签约最小金额')),
                ('maxprice', models.FloatField(default=0, verbose_name='签约最大金额')),
            ],
            options={
                'verbose_name': '客户签约申请记录',
                'verbose_name_plural': '客户签约申请记录',
            },
        ),
        migrations.CreateModel(
            name='BussinessMats',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('minprice', models.FloatField(default=0, verbose_name='签约最小金额')),
                ('maxprice', models.FloatField(default=0, verbose_name='签约最大金额')),
                ('monthly', models.BooleanField(default=False, verbose_name='是否允许月结')),
            ],
            options={
                'verbose_name': '企业签约',
                'verbose_name_plural': '企业签约',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('mobile', models.CharField(max_length=15, null=True, unique=True, verbose_name='手机号')),
                ('password', models.BinaryField(max_length=255, null=True, verbose_name='密码')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='姓名')),
                ('company', models.CharField(blank=True, db_index=True, max_length=100, null=True, verbose_name='公司名称')),
                ('is_buessini', models.BooleanField(default=False, verbose_name='是否是企业用户')),
                ('monthly', models.BooleanField(default=False, verbose_name='是否允许月结')),
                ('settlement_cycle', models.IntegerField(default=0, verbose_name='结算天数')),
                ('openid', models.CharField(blank=True, db_index=True, max_length=80, null=True, unique=True, verbose_name='微信唯一标识')),
                ('enable', models.BooleanField(default=True, verbose_name='是否启用')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('parent', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='belong_to', to='customer.Customer', verbose_name='归属于')),
            ],
            options={
                'verbose_name': '客户',
                'verbose_name_plural': '客户',
            },
        ),
        migrations.CreateModel(
            name='WXToken',
            fields=[
                ('openId', models.CharField(db_index=True, max_length=50, primary_key=True, serialize=False, unique=True, verbose_name='用户唯一标识')),
                ('access_token', models.CharField(db_index=True, max_length=200, null=True, unique=True, verbose_name='网页授权接口调用凭证')),
                ('expires_in', models.DateTimeField(null=True, verbose_name='有效期到')),
                ('refresh_token', models.CharField(db_index=True, max_length=200, null=True, unique=True, verbose_name='用户刷新access_token')),
                ('endTime', models.DateTimeField(null=True, verbose_name='有效期到')),
            ],
        ),
    ]
