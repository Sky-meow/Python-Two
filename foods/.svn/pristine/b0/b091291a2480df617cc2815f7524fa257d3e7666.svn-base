# encoding:utf-8
from django.db import transaction
from rest_framework import serializers
from custrole.models import *


class RoleSerializers(serializers.ModelSerializer):
    '''
    角色序列化
    '''
    customers = serializers.SerializerMethodField()

    def get_customers(self, obj):
        child = obj.custromerrole__set.all().values_list('customer', flat=False)
        from customer.models import Customer
        from customer.serializers import CustomerSerializers
        customers = Customer.objects.filter(id__in=child)
        return CustomerSerializers(customers, many=True).data

    class Meta:
        model = Role
        fields = '__all__'
