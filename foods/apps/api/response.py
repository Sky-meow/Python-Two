#encoding:utf-8
import coreapi
from django.utils import six
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend


class JsonResponse(Response):
    """
    An HttpResponse that allows its data to be rendered into
    arbitrary media types.
    """

    def __init__(self, data=None, code=200, desc='SUCCESS',
                 status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None):
        """
        Alters the init arguments slightly.
        For example, drop 'template_name', and instead use 'data'.
        Setting 'renderer' and 'media_type' will typically be deferred,
        For example being set automatically by the `APIView`.
        """
        super(Response, self).__init__(None, status=status)

        if isinstance(data, Serializer):
            msg = (
                'You passed a Serializer instance as data, but '
                'probably meant to pass serialized `.data` or '
                '`.error`. representation.'
            )
            raise AssertionError(msg)

        self.data = {"code": code, "desc": desc}
        if data is not None:
            if type(data) == dict:
                    for key in data:
                        if type(data[key]) == list:
                            for it in data[key]:
                                if type(it) == list:
                                    for k in it:
                                        if it[k] is None:
                                            it[k] = ''
                                else:
                                    it = ''
                        else:
                            if data[key] is None:
                                data[key] = ''
            else:
                pass
                
            self.data["data"] = data
        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type
        # self['Access-Control-Allow-Origin'] = '*'
        # self['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS, PUT, DELETE'
        # self['Access-Control-Max-Age'] = '1000'
        # self['Access-Control-Allow-Headers'] = '*'
        self['Access-Control-Allow-Credentials'] = True
        if headers:
            for name, value in six.iteritems(headers):
                self[name] = value

def api_paging(objs, request, Serializer):
    """
    objs : 实体对象
    request : 请求对象
    Serializer : 对应实体对象的序列化
    """
    from django.db.models.query import QuerySet
    from itertools import chain
    try:
        page_size = int(request.GET.get('page_size', 10))
        page = int(request.GET.get('page', 1))
    except (TypeError, ValueError):
        return JsonResponse(code=status.HTTP_400_BAD_REQUEST, desc='page and page_size must be integer!')
    if not objs.exists():
        return JsonResponse(code=status.HTTP_200_OK, desc='SUCCESS')
    paginator = Paginator(objs, page_size) # paginator对象
    if type(objs) == QuerySet:
        total = paginator.num_pages #总页数
    elif type(objs) == chain:
        count = 0
        for i in objs:
            count = count+1
        total = count
    try:
        objs = paginator.page(page)
    except PageNotAnInteger:
        objs = paginator.page(1)
    except EmptyPage:
        objs = paginator.page(paginator.num_pages)
        
    recode_count = paginator.count

    try:
        serializer = Serializer(objs, many=True) #序列化操作
        data = serializer.data
        # if data is not None:
        #     for item in data:
        #         for key in item:
        #             if type(item[key]) == list:
        #                 for it in item[key]:
        #                     if type(it) == list:
        #                         for k in it:
        #                             if it[k] is None:
        #                                 it[k] = ''
        #             else:
        #                 if item[key] is None:
        #                     item[key] = ''
        import json
        json_str = json.dumps(data, ensure_ascii=False)
        return JsonResponse(data={
            'detail': data,
            'list': json_str,
            'contacts': '{"data":'+json_str+'}',
            'page': page,
            'total': total,
            'page_size': page_size,
            'count': recode_count,
        }, code=status.HTTP_200_OK, desc='SUCCESS') #返回
    except Exception as e:
        raise e
        return JsonResponse(code=status.HTTP_400_BAD_REQUEST, desc='Error') #返回 

def DocParam(name="default", location="query",
             required=True, description=None, type="string",
             example = None,
             *args, **kwargs):
    return coreapi.Field(name=name, location=location,
                         required=required, description=description,
                         type=type, example=example)

def get_parameter_dic(request, coreapi_fields=None, *args, **kwargs):
    '''
    统一处理参数
    '''
    from django.http import QueryDict
    from rest_framework.request import Request

    if isinstance(request, Request) == False:
        return {}

    query_params = request.query_params
    if isinstance(query_params, QueryDict):
        query_params = query_params.dict()
    result_data = request.data
    if isinstance(result_data, QueryDict):
        result_data = result_data.dict()

    if query_params != {}:
        if coreapi_fields:
            for field in coreapi_fields:
                if field.required and  field.name not in query_params.keys():
                    return JsonResponse(code=400, desc=u"%s不能为空" % field.description)

        return query_params
    else:
        if coreapi_fields:
            for field in coreapi_fields:
                if field.required and  field.name not in result_data.keys():
                    return JsonResponse(code=400, desc=u"%s不能为空" % field.description)
                    
        return result_data

def get_content_type_for_model(obj):
    from django.contrib.contenttypes.models import ContentType
    return ContentType.objects.get_for_model(obj, for_concrete_model=False)

def log(request, message, flag='api', obj=None):
    from xadmin.models import Log
    log = Log(
        user=request.user,
        ip_addr=request.META['REMOTE_ADDR'],
        action_flag=flag,
        message=message
    )
    if obj:
        log.content_type = get_content_type_for_model(obj)
        log.object_id = obj.pk
        log.object_repr = force_text(obj)
    log.save()
