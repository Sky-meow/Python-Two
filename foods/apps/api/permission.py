# encoding:utf-8

from rest_framework import permissions
from rest_framework.request import Request as rfRequest
from rest_framework.authentication import BaseAuthentication
from api.models import customer_auth
from rest_framework import HTTP_HEADER_ENCODING, exceptions
from django.core.cache import cache
from django.core.handlers.wsgi import WSGIRequest
import datetime

def checkToken(func):
    def wrapper(request, *args, **kwargs):
        token = None
        if isinstance(request, WSGIRequest):
            if 'token' in request.GET.keys():
                token = request.GET['token']
            elif 'token' in request.POST.keys():
                token = request.POST['token']
        elif isinstance(request, rfRequest):
            params = _get_parameter_dic(request)
            if 'token' in params.keys():
                token = params['token']
        else:
            if 'token' in kwargs.keys():
                token = kwargs['token']
            else:
                if len(args) == 1:
                    params = _get_parameter_dic(args[0])
                    if 'token' in params.keys():
                        token = params['token']
                else:
                    for arg in args:
                        params = _get_parameter_dic(arg)
                        if 'token' in params.keys():
                            token = params['token']
                            break
        if token is None:
            return HttpResponse(
                json.dumps({
                    "result": False,
                    "data": [],
                    "desc": u"请先登陆",
                    "code": 403
                }, ensure_ascii=False), content_type='application/json')
            return JsonResponse(code=403, desc=u'请先登陆')
        try:
            token = customer_auth.objects.get(token=token)
            if not token.checkToken():
                return HttpResponse(
                    json.dumps({
                        "desc": u"Token已过期",
                        "code": 403
                    }, ensure_ascii=False), content_type='application/json')
                return JsonResponse(code=403, desc=u'Token已过期')
            else:
                request.login_user = token.customer
        except customer_auth.DoesNotExist:
            return HttpResponse(
                json.dumps({
                    "desc": u"Token信息不正确",
                    "code": 403
                }, ensure_ascii=False), content_type='application/json')
            return JsonResponse(code=403, desc=u'Token信息不正确')
        except Exception as e:
            return HttpResponse(
                json.dumps({
                    "desc": u"Token信息不正确",
                    "code": 403
                }, ensure_ascii=False), content_type='application/json')
            return JsonResponse(code=403, desc=u'Token信息不正确')
        return func(request, *args, **kwargs)
    return wrapper



def _get_parameter_dic(request, *args, **kwargs):
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
        return query_params
    else:
        return result_data
