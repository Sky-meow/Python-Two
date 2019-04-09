#encoding:utf-8

'''
微信请求的公共方法
'''
import hashlib
import random
import time
import datetime
import json
from urllib import parse
from xml.etree.ElementTree import fromstring
import requests
from weixinpay import wechatConfig
from django.db import transaction
from customer.models import Customer
from system.models import User
from customer.models import WXToken
from django.core.cache import cache

class WechatAPI(object):
    def __init__(self):
        self.config = wechatConfig
        self._access_token = None
        self.token_time = None
        self._openid = None

    @staticmethod
    def process_response_login(rsp):
        """解析微信登录返回的json数据，返回相对应的dict, 错误信息"""
        # print('****************url*******************')
        # print(rsp.url)
        # print('****************url*******************')

        if 200 != rsp.status_code:
            return None, {'code': rsp.status_code, 'msg': 'http error'}
        try:
            content = rsp.json()
            if 'errcode' in content.keys() and content['errmsg']!='ok':
                return None, content['errmsg']
        except Exception as e:
            return None, e
        if 'errcode' in content and content['errcode'] != 0:
            return None, content['errmsg']

        return content, None

    @staticmethod
    def create_time_stamp():
        """产生时间戳"""
        now = time.time()
        return int(now)

    @staticmethod
    def create_nonce_str(length=32):
        """产生随机字符串，不长于32位"""
        chars = "abcdefghijklmnopqrstuvwxyz0123456789"
        strs = []
        for x in range(length):
            strs.append(chars[random.randrange(0, len(chars))])
        return "".join(strs)

    @staticmethod
    def xml_to_array(xml):
        """将xml转为array"""
        array_data = {}
        root = fromstring(xml)
        for child in root:
            value = child.text
            array_data[child.tag] = value
        return array_data

    def array_to_xml(self, dic, sign_name=None):
        """array转xml"""
        if sign_name is not None:
            dic[sign_name] = self.get_sign()
        xml = ["<xml>"]
        for k in dic.keys():
            xml.append("<{0}>{1}</{0}>".format(k, dic[k]))
        xml.append("</xml>")
        return "".join(xml)

class WechatLogin(WechatAPI):
    def get_code_url(self, qs = None):
        """微信内置浏览器获取网页授权code的url"""
        r_url = self.config.REDIRECT_URI
        if qs is not None:
            r_url = r_url + '?' + qs
        url = self.config.defaults.get('wechat_browser_code') + (
            '?appid=%s&redirect_uri=%s&response_type=code&scope=%s&state=%s#wechat_redirect' %
            (self.config.APPID, parse.quote(r_url),
             self.config.SCOPE, self.config.STATE if self.config.STATE else ''))        
        return url

    def get_code_url_pc(self, qs = None):
        """pc浏览器获取网页授权code的url"""
        r_url = self.config.REDIRECT_URI
        if qs is not None:
            r_url = r_url + '?' + qs
        url = self.config.defaults.get('pc_QR_code') + (
            '?appid=%s&redirect_uri=%s&response_type=code&scope=%s&state=%s#wechat_redirect' %
            (self.config.APPID, parse.quote(r_url), self.config.PC_LOGIN_SCOPE,
             self.config.STATE if self.config.STATE else ''))
        return url

    def get_openId(self, code):
        """获取OpenId"""
        params = {
            'appid': self.config.APPID,
            'secret': self.config.APPSECRET,
            'code': code,
            'grant_type': 'authorization_code'
        }
        token, err = self.process_response_login(requests
                                                 .get(self.config.defaults.get('wechat_browser_access_token'),
                                                      params=params)) 
        
        if not err:
            self._access_token = token['access_token']
            self.token_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self._openid = token['openid']
            try:
                _token, create = WXToken.objects.get_or_create(openId = self._openid)
                _token.access_token = self._access_token
                _token.refresh_token = token['refresh_token']
                _token.expires_in = (datetime.datetime.now() + datetime.timedelta(seconds=7200)).strftime('%Y-%m-%d %H:%M:%S')
                _token.endTime = (datetime.datetime.now() + datetime.timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
                _token.save()
            except Exception as e:
                print('*************error***************')
                print(e)
                print('*************error***************')
                pass
            return self._openid , None
        else:
            return None , err

    def get_access_token(self,openId):
        """获取access_token"""
        token_cache_key = 'userinfo_access_token' #对不同的app指定不同的缓存
        token = cache.get(token_cache_key)
        if token:
            self._access_token = token['access_token']
            self._openid = token['openid']
            return self._access_token, self._openid
        else:
            try:
                _token = WXToken.objects.get(openId = openId) 
                if _token:
                    time = _token.expires_in 
                    time2 = _token.endTime
                    if time > datetime.datetime.now():
                        self._access_token = _token.access_token
                        self._openid = _token.openId
                        return self._access_token, self._openid
                    elif time <= datetime.datetime.now() and time2 > datetime.datetime.now():
                        params = {
                            'appid': self.config.APPID,
                            'refresh_token': _token.refresh_token,
                            'grant_type': 'refresh_token'
                        }
                        token, err = self.process_response_login(requests
                                                                .get(self.config.defaults.get('wechat_browser_refresh_token'),
                                                                    params=params))  
                        
                        cache.set(token_cache_key, token, token['expires_in']-60)
                        self._access_token = token['access_token']
                        self._openid = token['openid']
                        _token.access_token = self._access_token
                        _token.refresh_token = token['refresh_token']
                        _token.expires_in = (datetime.datetime.now() + datetime.timedelta(seconds=7200)).strftime('%Y-%m-%d %H:%M:%S')
                        _token.endTime = (datetime.datetime.now() + datetime.timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
                        _token.save()
                        return self._access_token, self._openid
            except:
                return None,None

    def get_user_info(self, access_token, openid):
        """获取用户信息"""
        params = {
            'access_token': access_token,
            'openid': openid,
            'lang': self.config.LANG
        }
        return self.process_response_login(requests
                                           .get(self.config.defaults.get('wechat_browser_user_info'), params=params))

    def get_total_access_token(self):
        '''
        获取全局权限使用的access_token
        '''
        from syssetting.models import WeChatToken
        token_cache_key = 'total_access_token' #对不同的app指定不同的缓存
        token = cache.get(token_cache_key)
        if token:
            return token, None
        
        params = {
            'grant_type': 'client_credential',
            'appid': self.config.APPID,
            'secret': self.config.APPSECRET
        }
        token, err = self.process_response_login(requests
                                                    .get(self.config.defaults.get('wechat_total_access_token'),
                                                        params=params))  
        if not err:
            access_token = token['access_token']
            expires_in = token['expires_in']
            if access_token and expires_in:
                cache.set(token_cache_key, access_token, expires_in-60)
                time = expires_in
                try:
                    _token ,create = WeChatToken.objects.get_or_create(access_token=access_token)                    
                    _token.expires_in = (datetime.datetime.now() + datetime.timedelta(seconds=7200)).strftime('%Y-%m-%d %H:%M:%S')
                    _token.save()
                except Exception as e:
                    print('*********db error**********')
                    print(e)
                    print('*********db error**********')
            return access_token , None
        else:
            return None , err



from rest_framework.views import APIView
from django.http import HttpResponseRedirect
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render, redirect
from api.response import JsonResponse
from rest_framework.response import Response

class WechatViewSet(APIView):
    wechat_api = WechatLogin()

class OpenIdView(WechatViewSet):
    def get(self, request):
        if 'code' in request.query_params.keys():
            code = request.query_params.get('code')
            data,err = self.wechat_api.get_openId(code)
            if not err:
                return JsonResponse(data={'openid':data})
            else:
                return JsonResponse(code=400,desc=err)
        else:
            return JsonResponse(code=400,desc=u'请先授权')

class AuthView(WechatViewSet):
    def get(self, request):
        url = ''
        if 'from' in request.GET.keys():
            par = request.GET['from']
            url = self.wechat_api.get_code_url('from='+par)
        else:
            url = self.wechat_api.get_code_url()
        return redirect(url)

class GetInfoView(WechatViewSet):
    def get(self, request):
        if 'openid' in request.query_params.keys():
            if request.query_params.get('openid') == '':
                return JsonResponse(code=400,desc=u'openid不能为空')
            token,openid = self.wechat_api.get_access_token(request.query_params.get('openid'))
            user_info, error = self.wechat_api.get_user_info(token, openid)
            if error:
                return JsonResponse(code=400,desc=error)
            user_data = {
                'nickname': user_info['nickname'].encode('iso8859-1').decode('utf-8'),
                'sex': user_info['sex'],
                'province': user_info['province'].encode('iso8859-1').decode('utf-8'),
                'city': user_info['city'].encode('iso8859-1').decode('utf-8'),
                'country': user_info['country'].encode('iso8859-1').decode('utf-8'),
                'avatar': user_info['headimgurl'],
                'openid': user_info['openid']
            }
            try:
                cust = User.objects.get(openid=openid)
                if cust.Parent is not None:
                    p = cust.Parent
                else:
                    p = cust
                project = p.projects_set.all().values('ID','Name').first()
                if project is not None:
                    user_data['Mobile'] = cust.Mobile
                    user_data['projectId'] = project['ID']
                    user_data['project'] = project['Name']
            except User.DoesNotExist:
                cust , create = Customer.objects.get_or_create(openid=openid,Enable=True)
                if not create:
                    if cust.Parent is not None:
                        if cust.Parent.Project_id and cust.Parent.Project is not None:
                            user_data['projectId'] = cust.Parent.Project.ID
                            user_data['project'] = str(cust.Parent.Project)
                            user_data['is_buessini'] = cust.Parent.is_buessini
                            user_data['monthly'] = cust.Parent.monthly
                            user_data['Settlement_cycle'] = cust.Parent.Settlement_cycle
                    else:
                        if cust.Project_id and cust.Project is not None:
                            user_data['projectId'] = cust.Project.ID
                            user_data['project'] = str(cust.Project)
                            user_data['is_buessini'] = cust.is_buessini
                            user_data['monthly'] = cust.monthly
                            user_data['Settlement_cycle'] = cust.Settlement_cycle
                    

                    user_data['parent'] = str(cust.Parent)
                    user_data['Mobile'] = cust.Mobile
                    user_data['Company'] = cust.Company
            except Exception as e:
                return JsonResponse(code=400,desc=u'内部错误:%s'%e.args)

            return JsonResponse(data=user_data)
        else:
            return JsonResponse(code=400,desc=u'openid不能为空')

class GetTotalAccessToken(WechatViewSet):
    '''
    获取整体的access_token
    '''
    TOKEN_CACHE_PRE = 'total'

    def get(self,request):
        token , err = self.wechat_api.get_total_access_token()
        if not err:
            return JsonResponse()
        else:
            return JsonResponse(code=400,desc=err)

class GetSignature(WechatViewSet):
    '''
    获取js-sdk的使用权限签名
    '''
    def get(self,request):
        if 'url' not in request.query_params.keys():
            return JsonResponse(code=400,desc=u'请传入当前url')
        url = request.query_params.get('url')
        signature_cache_key = 'signature_'+url+'_cache'
        cache.delete(signature_cache_key)
        signature_cache = cache.get(signature_cache_key)
        if signature_cache:
            jsapi_ticket = signature_cache
        else:
            token , err = self.wechat_api.get_total_access_token()
            if not err:
                params = {
                    'access_token': token,
                    'type': 'jsapi'
                }
                jsapi, err = self.wechat_api.process_response_login(requests
                                                        .get(self.wechat_api.config.defaults.get('wechat_jsapi_ticket'),
                                                            params=params))  
                if err:
                    return JsonResponse(code=400,desc=err) 
                else:
                    jsapi_ticket = jsapi['ticket']
                    expires_in = jsapi['expires_in']
                    cache.set(signature_cache_key, jsapi_ticket, expires_in-60)
            else:
                return JsonResponse(code=400,desc=err)

        import time
        import hashlib
        noncestr = self.wechat_api.create_nonce_str(16)
        timestamp = int(time.mktime(datetime.datetime.now().timetuple()))
        string = 'jsapi_ticket=%s&noncestr=%s&timestamp=%s&url=%s'%(jsapi_ticket,noncestr,timestamp,url)
        signature = hashlib.sha1(string.encode('utf8')).hexdigest()
        data = {
            'timestamp': timestamp,
            'noncestr': noncestr,
            'signature': signature,
            'appid': self.wechat_api.config.APPID,  
            'jsapi_ticket': jsapi_ticket,
            'string1': string                      
        }
        return JsonResponse(data=data)
