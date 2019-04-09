# encoding:utf-8
import xadmin
from django.db import transaction
from customer.models import *

'''
注解
'''


class CustomerAdmin(object):
    list_display = []  # 列表上显示的字段
    search_fields = []  # 模糊查询字段
    list_filter = []  # 过滤字段
    list_editable = []  # 列表中可编辑的字段
    readonly_fields = []  # 只读字段包括编辑/修改/新增页面
    inlines = []  # 额外的编辑表单
    ordering = []  # 排序字段

    def queryset(self):
        '''
        继承父类的查询方法
        '''
        queryset = super().queryset()  # 调用父类的查询方法
        #queryset = queryset.filter()
        return queryset()

    def save_models(self):
        '''
        保存事件
        '''
        super().save_models()


xadmin.site.register(Customer, CustomerAdmin)
