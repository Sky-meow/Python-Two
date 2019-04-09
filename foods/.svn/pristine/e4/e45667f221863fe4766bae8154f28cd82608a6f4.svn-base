# encoding:utf-8

'''
用户的api集合
'''
import coreapi
from django.db import transaction
from api.response import api_paging, JsonResponse, log, DocParam, get_parameter_dic
from api.permission import checkToken
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet as mvs
from rest_framework.views import APIView
from rest_framework.decorators import (
    api_view, permission_classes, detail_route, action, list_route
)
from rest_framework.permissions import AllowAny
from customer.models import *
from customer.serializers import *
from django.db.models import Q
from datetime import datetime
from django.utils.decorators import method_decorator

# 针对类下面所有的方法都使用checkToken装饰器
@method_decorator(checkToken, name='dispatch')
class get_customers(APIView):
    '''
    获取用户列表
    '''
    coreapi_fields = (
        DocParam('search', required=False, type='string',
                 description=u'模糊搜索字段,根据mobile,name,company,email检索'),
        DocParam('store', required=False, type='int',
                 description=u'根据签约的store进行检索'),
        DocParam('enable', required=False, type='bool',
                 description=u'用户状态,Ture是启用,False是停用,默认是启用状态'),
    )

    def post(self, request):
        pass

    def get(self, request):
        params_dict = dict()
        params_dict = {}
        #type(params_dict) == dict()
        #isinstance(params_dict, dict())
        params_list = list()  # []
        list(params_dict.keys())
        params = get_parameter_dic(request)
        queryset = Customer.objects.all()
        if 'status' in params.keys():
            if params['status'] == -1 or params['status'] == '-1':
                pass
            else:
                queryset = queryset.filter(status=params['status'])
                #a = [] + []
                # *args 表示参数是数组
                # **kwargs 表示参数是字典
                #dic = dict(dic1, **dic2)
        if 'identity' in params.keys() and params['identity'] in ['seller', 'service', 'norm']:
            if params['identity'] == 'seller':
                queryset = queryset.filter(is_seller=True)
            elif params['identity'] == 'service':
                queryset = queryset.filter(is_service=True)
            elif params['identity'] == 'norm':
                queryset = queryset.exclude(is_seller=True, is_service=True)
        # django.db.models.F 封装了 数据库的+-*/方法转义
        # queryset.filter(count=F('total')+F('sub')-*/)
        # __isnull =True / Flase  __icontains 不区分大小写的 like '%%'
        # __contains 区分大小写的 like '%%'
        if 'search' in params.keys():
            queryset = queryset.filter(
                Q(mobile__icontains=params['search']) | Q(nickname__icontains=params['search']) |
                Q(company__icontains=params['search']) | Q(
                    mail__icontains=params['search'])
            )
            '''
            queryset.count()记录数
            queryset.exists()是否存在
            queryset.distinct() 去重
            '''
            try:
                Customer.objects.get(pk=1)
            except Customer.DoesNotExist:
                pass
            except Exception as e:
                pass

        return api_paging(queryset, request, CustomerSerializers)


@method_decorator(checkToken, name='dispatch')
class AddressViewSet(viewsets.ModelViewSet):
    '''
    地址管理视图集
    '''
    queryset = Address.objects.all()
    serializer_class = AddressSerializers

    def list(self, request):
        return super().list(request)

    @detail_route(methods=['get', 'post'])
    def detail(self, request, pk=None):
        '''
        detail_route装饰器表示根据主键获取/执行一些操作
        methods 是该方法支持的请求类型
        pk是主键
        '''
        try:
            addr = self.queryset.get(pk=pk)
            serializer = self.serializer_class(addr)
            return JsonResponse(data=serializer.data)
        except Address.DoesNotExist:
            return JsonResponse(code=400, desc='地址不存在')
        except Exception as e:
            return JsonResponse(code=400, desc='系统错误 %s' % e)

    @list_route()
    def test(self, request):
        '''
        获取列表,该装饰器需用传入pk(主键)参数
        '''
        pass


@api_view(['GET'])
@checkToken  # 统一检测token是否有效的装饰器
@transaction.atomic()
def functions(request):
    '''
    另一种定义api的方法
    '''
    # TODO...
    with transaction.atomic():
        try:
            pass
        except:
            pass
