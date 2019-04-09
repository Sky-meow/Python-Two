#encoding:utf-8

from django.db import transaction 
from rest_framework import serializers
from order.models import Order,OrderItems
from material.serializers import MaterialSerializers,BentoSerializers
from customer.serializers import AddressSerializers


class OrderItemsSerializers(serializers.ModelSerializer):
    '''
    订单详情
    '''
    matlist = serializers.SerializerMethodField()
    def get_matlist(self,obj):
        import json
        if obj.materials is not None or obj.materials != '':
            return json.loads(obj.materials)
        else:
            return ''

    class Meta:
        model = OrderItems
        fields = '__all__'

class OrderSerializers(serializers.ModelSerializer):
    '''
    订单
    '''
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    confirm_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    cancel_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    complate_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    paied_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    prepay_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    
    items = serializers.SerializerMethodField()
    def get_items(self, obj):
        items = obj.order_items.all()
        return OrderItemsSerializers(items, many=True).data


    class Meta:
        model = Order
        fields = '__all__'
     