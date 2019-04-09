# encoding:utf-8
import uuid
from django.db import models

# Create your models here.


class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(
        "customer.Customer", verbose_name='所属用户', on_delete=models.CASCADE, db_constraint=False)
    role_name = models.CharField(verbose_name='角色名', null=False, max_length=50)
    subsidy = models.FloatField('角色补贴', default=0)

    def __str__(self):
        return '%s 补贴金额:%.2f' % (self.role_name, self.subsidy)

    class Meta:
        ordering = ('customer', )


class CustromerRole(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.OneToOneField(
        "customer.Customer", verbose_name='用户', on_delete=models.CASCADE, db_constraint=False)
    role = models.ForeignKey(
        "custrole.Role", verbose_name='角色', on_delete=models.CASCADE, db_constraint=False)

    class Meta:
        ordering = ('role', )
