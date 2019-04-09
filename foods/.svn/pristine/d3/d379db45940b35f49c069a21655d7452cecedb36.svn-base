# encoding:utf-8

from django.db import transaction
from rest_framework import serializers
from material.models import *


class MaterialSerializers(serializers.ModelSerializer):
    '''
    商品信息
    '''
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        images = {}
        if obj.image is not None:
            images["avatar"] = obj.image["avatar"].url
            images["avatar_nocrop"] = obj.image["avatar_nocrop"].url
            images["64"] = obj.image["64"].url
            images["128"] = obj.image["128"].url
            images["big"] = obj.image["big"].url
            images["big_nocrop"] = obj.image["big_nocrop"].url
            images["huge"] = obj.image["huge"].url
            images["huge_nocrop"] = obj.image["huge_nocrop"].url

        return images

    class Meta:
        model = Material
        fields = '__all__'


class MatTypeSerializers(serializers.ModelSerializer):
    '''
    商品类别
    '''
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = MatType
        fields = '__all__'
