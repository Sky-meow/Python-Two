import xadmin
from order.models import *

class order_Admin(object):
    list_display = ['name'] #列表中要展示的列
    search_fields = ['name'] #模糊搜索字段集合
    list_filter = [] #过滤字段
    list_editer = [] #列表中可编辑的页面
    readonly_fields = [] #只读字段

    
    def queryset(self):
        '''
        重写获取数据的方法
        '''
        queryset = super().queryset() #获取父级的queryset
        queryset = queryset.filter(name__icontains='tian') 
        return queryset


    def get_bypk(self,i):
        return Order.objects.filter(pk=i)

    def get_ordertype(self,i):
        return Order.objects.filter(order_type=i)


xadmin.site.register(Order, order_Admin)

class orderItems_Admin(object):
    list_display = ['name'] #列表中要展示的列
    search_fields = ['name'] #模糊搜索字段集合
    list_filter = [] #过滤字段
    list_editer = [] #列表中可编辑的页面
    readonly_fields = [] #只读字段

    def queryset(self):

        return super().queryset().filter(name__icontains='tian')


    def get_bypk(self,i):
        return OrderItems.objects.filter(pk=i)

xadmin.site.register(OrderItems, orderItems_Admin)
