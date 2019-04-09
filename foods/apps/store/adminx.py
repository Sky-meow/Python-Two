import xadmin
from django.db import transaction
from django.forms import ModelMultipleChoiceField
from .models import *
from django.conf import settings


if "material" in settings.INSTALLED_APPS:
    class StoreMatsInline(object):
        model = StoreMats
        extra = 1
        #exclude = ['created_at', 'updated_at']
        style = 'one'
        #fields = ['material']


class StoreAdmin(object):
    list_display = ['name', 'address',
                    'scope', 'enable', 'fee', 'minQty', 'preferential', 'head']
    search_fields = ['name', 'address', 'head__userame', 'head__mobile']
    list_filter = ['scope', 'enable', 'fee', 'head']
    list_editable = ['scope', 'enable', 'fee']
    address_fields = ['address']
    style_fields = {"address": "address"}
    if "material" in settings.INSTALLED_APPS:
        inlines = [StoreMatsInline, ]


xadmin.site.register(Store, StoreAdmin)


if "material" in settings.INSTALLED_APPS:
    def get_materila_name(m):
        return '[%d元] %s-%s' % (int(m.price), str(m.mattype), m.name)

    class MaterialMultipleChoiceField(ModelMultipleChoiceField):
        def label_from_instance(self, m):
            return get_materila_name(m)

    class StoreMatsAdmin(object):
        list_display = ['store', 'material', 'enable_from', 'enable_to']
        search_fields = ['store__name', 'material__SKU', 'material__name']
        list_filter = ['enable_from', 'enable_to']
        list_editable = ['enable_from', 'enable_to']
        style_fields = {'material': 'm2m_transfer'}

        def get_field_attrs(self, db_field, **kwargs):
            attrs = super().get_field_attrs(db_field, **kwargs)
            if db_field.name == 'material':
                attrs['form_class'] = MaterialMultipleChoiceField
            return attrs

    xadmin.site.register(StoreMats, StoreMatsAdmin)
