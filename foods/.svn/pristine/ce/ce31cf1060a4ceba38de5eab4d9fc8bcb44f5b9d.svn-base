# encoding:utf-8

from django.db import transaction
from rest_framework import serializers

from system.models import *


class UserSerializers(serializers.ModelSerializer):

    avatars = serializers.SerializerMethodField()

    def get_avatars(self, obj):
        avatars = {}
        if obj.cover is not None:
            avatars["avatar"] = obj.avatar["avatar"].url
            avatars["avatar_nocrop"] = obj.avatar["avatar_nocrop"].url
            avatars["64"] = obj.avatar["64"].url
            avatars["128"] = obj.avatar["128"].url
            avatars["big"] = obj.avatar["big"].url
            avatars["big_nocrop"] = obj.avatar["big_nocrop"].url
            avatars["huge"] = obj.avatar["huge"].url
            avatars["huge_nocrop"] = obj.avatar["huge_nocrop"].url

        return avatars

    class Meta:
        model = User
        fields = '__all__'
