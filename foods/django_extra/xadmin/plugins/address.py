#encoding:utf-8
'''
地址录入插件
集成高德地图的AutoComplate功能
'''
import xadmin
from django import forms
from django.conf import settings
from django.db.models import CharField
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from xadmin.views.edit import ModelFormAdminUtil
from xadmin.views import BaseAdminPlugin, CreateAdminView, UpdateAdminView

class XAdminAddressWidget(forms.TextInput):
    """
    用于替换普通输入框的带高德自动填充的输入框
    """
    def __init__(self, attrs={}):
        super(XAdminAddressWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):     
        context = super().get_context(name, value, attrs)
        context['widget']['type'] = self.input_type
        return mark_safe(render_to_string('xadmin/address/text.html', context))


class XAdminCityWidget(forms.TextInput):
    """
    用于替换普通输入框的带高德自动填充的输入框
    """
    def __init__(self, attrs={}):
        super(XAdminCityWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):     
        context = super().get_context(name, value, attrs)
        context['widget']['type'] = self.input_type
        return mark_safe(render_to_string('xadmin/address/select.html', context))

class AddressPlug(BaseAdminPlugin):
    # address_fields = []

    # def init_request(self, *args, **kwargs):
    #     active = bool(self.request.method == 'GET' and self.admin_view.has_change_permission() and self.address_fields)
    #     if active:
    #         self.model_form = self.get_model_view(ModelFormAdminUtil, self.model).form_obj
    #     return active

    def get_field_style(self, attrs, db_field, style, **kwargs):
        if style == 'address':
            if isinstance(db_field, CharField):
                widget = db_field.formfield().widget
                return {'widget': XAdminAddressWidget(widget.attrs)}
        elif style == 'cityselect':
            if isinstance(db_field, CharField):
                widget = db_field.formfield().widget
                return {'widget': XAdminCityWidget(widget.attrs)}

        return attrs
       
    def block_extrahead(self, context, nodes):  # 在生成的页面中加入自定义的 js 文件
        _js = '<script type="text/javascript" src="%s&key=%s&plugin=AMap.Autocomplete,AMap.DistrictSearch"></script>' % (settings.GAODEMAP_URL, settings.GAODEMAP_KEY)
        nodes.append(_js)

xadmin.site.register_plugin(AddressPlug, CreateAdminView)
xadmin.site.register_plugin(AddressPlug, UpdateAdminView)

from xadmin.plugins.inline import AccInlineStyle,InlineStyleManager

style_manager = InlineStyleManager()

class AddresslineStyle(AccInlineStyle):
    template = 'xadmin/address/edit_inline/accordion.html'

style_manager.register_style("address_accordion", AddresslineStyle)
