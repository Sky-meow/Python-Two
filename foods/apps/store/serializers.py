#encoding:utf-8

from django.conf import settings
from rest_framework import serializers

from store.models import *


class StorePickTimeSerializers(serializers.ModelSerializer):

    pickup_time = serializers.SerializerMethodField()
    def get_pickup_time(self, obj):
        return str(obj)

    class Meta:
        models = StorePickTime
        fields = '__all__'
        
class StoreSerializers(serializers.ModelSerializer):

    pickup_times = serializers.SerializerMethodField()
    def get_pickup_times(self, obj):
        return StorePickTimeSerializers(obj.store.store_pickup_times, many=True).data

    class Meta:
        models = Store
        fields = '__all__'
    
if "material" in settings.INSTALLED_APPS:
    from material.serializers import MaterialSerializers
    class StoreMatsSerializers(serializers.ModelSerializer):
        enable_from = serializers.DateField(format='%Y-%m-%d')
        enable_to = serializers.DateField(format='%Y-%m-%d')

        created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
        updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

        mat = serializers.SerializerMethodField()
        def get_mat(self, obj):
            return MaterialSerializers(obj.material).data
        

        class Meta:
            models = StoreMats
            fields = '__all__'