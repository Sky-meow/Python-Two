# encoding:utf-8

from django.db import transaction
from rest_framework import serializers
from customer.models import Customer, SendingCust, Address, BuesinessApply
from store.serializers import ProjectsSerializers


class CustomerSerializers(serializers.ModelSerializer):
    '''
    个人用户信息
    '''
    # child = serializers.SerializerMethodField()
    # def get_child(self, obj):
    #     child = obj.belong_to.all()#Customer.objects.filter(parent=obj)
    #     return SendingCustSerializers(child, many=True).data

    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Customer
        fields = '__all__'


class AddressSerializers(serializers.ModelSerializer):
    '''
    客户送餐地址
    '''

    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Address
        fields = '__all__'


class SendingCustSerializers(serializers.ModelSerializer):
    '''
    员工用户信息
    '''
    child = serializers.SerializerMethodField()

    def get_child(self, obj):
        child = obj.belong_to.all()  # Customer.objects.filter(parent=obj)
        return SendingCustSerializers(child, many=True).data

    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = SendingCust
        fields = '__all__'


class BuesinessApplySerializers(serializers.ModelSerializer):
    '''
    签约申请记录
    '''

    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = BuesinessApply
        fields = '__all__'
