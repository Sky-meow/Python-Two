# encoding:utf-8
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import (action, api_view, detail_route,
                                       list_route, permission_classes)
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from api.response import DocParam, JsonResponse, api_paging,get_parameter_dic, log


# from api.models import customer_auth

__all__ = [
    'JsonResponse','api_paging','DocParam','get_parameter_dic','log',
    'AllowAny', 'action', 'api_view', 'detail_route',
    'list_route', 'permission_classes', 'APIView', 'Q'
]
