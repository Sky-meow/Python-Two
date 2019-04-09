import xadmin
from custrole.models import *

class Role_Admin(object):
    list_display = ['name'] #列表中要展示的列
    search_fields = ['name'] #模糊搜索字段集合
    list_filter = [] #过滤字段
    list_editer = [] #列表中可编辑的页面
    readonly_fields = [] #只读字段

    def queryset(self):
        
        queryset = super().queryset().filter(name__icontains='none') 

    def get_bypk(self,i):
        return Role.objects.filter(pk=i)

xadmin.site.register(Role, Role_Admin)

class CustromerRole_Admin(object):
    list_display = ['name'] #列表中要展示的列
    search_fields = ['name'] #模糊搜索字段集合
    list_filter = [] #过滤字段
    list_editer = [] #列表中可编辑的页面
    readonly_fields = [] #只读字段


xadmin.site.register(CustromerRole, CustromerRole_Admin)
