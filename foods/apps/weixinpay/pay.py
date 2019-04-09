#encoding:utf-8
import json
import time
import uuid
from collections import defaultdict
from hashlib import md5
from weixinpay import wechatConfig
import dicttoxml
import requests
import xmltodict


class Wxpay(object):
    from django.conf import settings
    DEBUG = settings.DEBUG
    if DEBUG:
        UNIFIEDORDER_URL = 'https://api.mch.weixin.qq.com/sandboxnew/pay/unifiedorder' #预支付
        ORDERQUERY_URL = 'https://api.mch.weixin.qq.com/sandboxnew/pay/orderquery' #订单查询
        REFUND_URL = 'https://api.mch.weixin.qq.com/sandboxnew/pay/refund' #退款申请
    else:
        UNIFIEDORDER_URL = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
        ORDERQUERY_URL = 'https://api.mch.weixin.qq.com/pay/orderquery'
        REFUND_URL = 'https://api.mch.weixin.qq.com/secapi/pay/refund'
        CLOSEORDER_URL = 'https://api.mch.weixin.qq.com/pay/closeorder' #关闭订单
        WX_CERT_PATH = "/Apps/aaa/afdklfsiewr.pem"
        WX_KEY_PATH = "/Apps/aaa/bjkldfjlkas.pem"
        WX_CA_PATH = "/Apps/aaa/rootca.pem"

    def __init__(self):
        u"""
        args:
            appid: 应用id
            mch_id: 商户号
            key: API密钥
        """
        self.appid = wechatConfig.APPID
        self.mch_id = wechatConfig.MCH_ID
        self.key = wechatConfig.API_KEY
        self.sandbox_key = ''
        self.default_params = {
            'appid': wechatConfig.APPID,
        }

    def logged(self,content):
        '''
        保存日志
        '''
        pass
        import os
        import logging
        from django.conf import settings
        logging.basicConfig(filename=os.path.join(settings.BASE_DIR+'/logs/','debug.txt'),level=logging.DEBUG)
        filename = settings.BASE_DIR+'/logs/log.txt'
        f = open(filename,'a',encoding='utf-8')
        f.write(content)
        f.write('\n')
        f.close()

    def _generate_nonce_str(self):
        u"""生成随机字符串
        """
        return str(uuid.uuid4()).replace('-', '')

    def generate_sign(self, params, key=None):
        u"""生成md5签名的参数
        """
        if key is None:
            key = self.key

        src = '&'.join(['%s=%s' % (k, v) for k,
                        v in sorted(params.items())]) + '&key=%s' % key
        #self.logged('sign_str::::%s'%src)
        return md5(src.encode('utf-8')).hexdigest().upper()

    def generate_request_data(self, **kwargs):
        u"""生成统一下单请求所需要提交的数据
        https://pay.weixin.qq.com/wiki/doc/api/app/app.php?chapter=9_1
        trade_type为JSAPI时候,必须传入 用户标识 openid
        trade_type=NATIVE时,必须传入product_id,该ID对应扫描的二维码中对应的商品ID
        """
        params = self.default_params.copy()
        params['mch_id'] = self.mch_id
        params['fee_type'] = 'CNY'
        params['device_info'] = 'WEB'
        params['trade_type'] = 'JSAPI' #公众号支付   NATIVE:扫码支付  APP:APP支付
        params['nonce_str'] = self._generate_nonce_str()
        #params['notify_url'] = self.notify_url
        params.update(kwargs)
        if self.DEBUG:
            if self.sandbox_key == '':
                d = {
                    'mch_id' : self.mch_id,
                    'nonce_str' : self._generate_nonce_str(),
                }
                d['sign'] = self.generate_sign(d)
                xml_d = '<xml>%s</xml>' % dicttoxml.dicttoxml(d, root=False)
                headers = {'Content-Type': 'application/xml'}
                res = requests.post('https://api.mch.weixin.qq.com/sandboxnew/pay/getsignkey', data=xml_d, headers=headers)            
                result = json.loads(json.dumps(xmltodict.parse(res.text)))
                if result['xml']['return_code'] == 'SUCCESS':    
                    self.sandbox_key = result['xml']['sandbox_signkey'] 
                else:
                    return result['xml']['return_msg']
            params['sign'] = self.generate_sign(params,self.sandbox_key)
        else:
            params['sign'] = self.generate_sign(params)

        return '<xml>%s</xml>' % dicttoxml.dicttoxml(params, root=False)

    def generate_prepay_order(self, **kwargs):
        u"""生成预支付交易单
        签名后的数据请求 URL地址：https://api.mch.weixin.qq.com/pay/unifiedorder
        """
        headers = {'Content-Type': 'application/xml'}
        data = self.generate_request_data(**kwargs)
        
        #self.logged(str(data))
        res = requests.post(self.UNIFIEDORDER_URL, data=data, headers=headers)

        if res.status_code != 200:
            return defaultdict(str),None

        result = json.loads(json.dumps(xmltodict.parse(res.content)))

        # self.logged(str(result))
        if result['xml']['return_code'] == 'SUCCESS':
            return result['xml'],None
        else:            
            if 'return_msg' in result['xml'].keys():
                return None,result['xml']['return_msg']
            elif 'retmsg' in result['xml'].keys():
                return None,result['xml']['retmsg']

    def generate_call_jsapi_data(self,prepayid):
        '''
        生成微信内H5调起支付的请求参数
        args:
            prepayid: 预支付交易单
        https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=7_7&index=6
        '''
        params = dict()#self.default_params.copy()
        params['appId'] = self.appid
        params['package'] = 'prepay_id=%s'%str(prepayid)
        params['signType'] = 'MD5'

        if self.DEBUG:
            if self.sandbox_key == '':
                d = {
                    'mch_id' : self.mch_id,
                    'nonce_str' : self._generate_nonce_str(),
                }
                d['sign'] = self.generate_sign(d)
                xml_d = '<xml>%s</xml>' % dicttoxml.dicttoxml(d, root=False)
                headers = {'Content-Type': 'application/xml'}
                res = requests.post('https://api.mch.weixin.qq.com/sandboxnew/pay/getsignkey', data=xml_d, headers=headers)            
                result = json.loads(json.dumps(xmltodict.parse(res.text)))
                if result['xml']['return_code'] == 'SUCCESS':    
                    self.sandbox_key = result['xml']['sandbox_signkey'] 
                else:
                    return result['xml']['return_msg']
            
            params['nonceStr'] = self._generate_nonce_str()
            params['timeStamp'] = str(int(time.time()))
            params['paySign'] = self.generate_sign(params,self.sandbox_key)

        else:
            params['nonceStr'] = self._generate_nonce_str()
            params['timeStamp'] = str(int(time.time()))
            params['paySign'] = self.generate_sign(params)

        # self.logged(str(params))
        return params

    def generate_call_app_data(self, prepayid):
        u""""生成调起客户端app的请求参数
        args:
            prepayid: 预支付交易单
        https://pay.weixin.qq.com/wiki/doc/api/app/app.php?chapter=9_12&index=2
        """
        params = self.default_params.copy()
        params['partnerid'] = self.mch_id
        params['package'] = 'Sign=WXPay'
        params['noncestr'] = self._generate_nonce_str()
        params['timestamp'] = str(int(time.time()))
        params['prepayid'] = str(prepayid)
        params['sign'] = self.generate_sign(params)

        return params

    def generate_refund_data(self, transaction_id='', out_trade_no='', amt = 0):
        '''
        生成退款申请的数据
        '''
        params = self.default_params.copy()
        params['mch_id'] = self.mch_id
        params['nonce_str'] = self._generate_nonce_str()
        #params['timeStamp'] = str(int(time.time()))
        #params['sign_type'] = 'MD5'     
        params['transaction_id'] = transaction_id
        params['out_trade_no'] = out_trade_no
        params['out_refund_no'] = out_trade_no
        params['total_fee'] = 101 if self.DEBUG else amt
        params['refund_fee'] = 101 if self.DEBUG else amt
        if self.DEBUG:
            if self.sandbox_key == '':
                d = {
                    'mch_id' : self.mch_id,
                    'nonce_str' : self._generate_nonce_str(),
                }
                d['sign'] = self.generate_sign(d)
                xml_d = '<xml>%s</xml>' % dicttoxml.dicttoxml(d, root=False)
                headers = {'Content-Type': 'application/xml'}
                res = requests.post('https://api.mch.weixin.qq.com/sandboxnew/pay/getsignkey', data=xml_d, headers=headers)            
                result = json.loads(json.dumps(xmltodict.parse(res.text)))
                if result['xml']['return_code'] == 'SUCCESS':    
                    self.sandbox_key = result['xml']['sandbox_signkey'] 
                else:
                    return result['xml']['return_msg']
            params['sign'] = self.generate_sign(params,self.sandbox_key)
        else:
            params['sign'] = self.generate_sign(params)

        return '<xml>%s</xml>' % dicttoxml.dicttoxml(params, root=False)

    def generate_query_data(self, transaction_id='', out_trade_no=''):
        u"""生成查询订单的数据
        """
        params = self.default_params.copy()
        params['mch_id'] = self.mch_id
        params['nonce_str'] = self._generate_nonce_str()

        if transaction_id != '' and transaction_id is not None:
            params['transaction_id'] = transaction_id
        elif out_trade_no != '' and out_trade_no is not None:
            params['out_trade_no'] = out_trade_no
        else:
            raise Exception(
                'generate_query_data need transaction_id or out_trade_no')
        if self.DEBUG:
            if self.sandbox_key == '':
                d = {
                    'mch_id' : self.mch_id,
                    'nonce_str' : self._generate_nonce_str(),
                }
                d['sign'] = self.generate_sign(d)
                xml_d = '<xml>%s</xml>' % dicttoxml.dicttoxml(d, root=False)
                headers = {'Content-Type': 'application/xml'}
                res = requests.post('https://api.mch.weixin.qq.com/sandboxnew/pay/getsignkey', data=xml_d, headers=headers)            
                result = json.loads(json.dumps(xmltodict.parse(res.text)))
                if result['xml']['return_code'] == 'SUCCESS':    
                    self.sandbox_key = result['xml']['sandbox_signkey'] 
                else:
                    return result['xml']['return_msg']
            params['sign'] = self.generate_sign(params,self.sandbox_key)
        else:
            params['sign'] = self.generate_sign(params)

        return '<xml>%s</xml>' % dicttoxml.dicttoxml(params, root=False)

    def order_query_result(self, transaction_id='', out_trade_no=''):
        u"""查询订单
        args:
            transaction_id: 微信订单号(优先使用）
            out_trade_no: 商户订单号
        https://pay.weixin.qq.com/wiki/doc/api/app/app.php?chapter=9_2&index=4
        """
        headers = {'Content-Type': 'application/xml'}
        data = self.generate_query_data(
            transaction_id=transaction_id, 
            out_trade_no=out_trade_no
        )

        res = requests.post(self.ORDERQUERY_URL, data=data, headers=headers)
        
        if res.status_code != 200:
            return defaultdict(str),None

        result = json.loads(json.dumps(xmltodict.parse(res.content)))

        if result['xml']['return_code'] == 'SUCCESS':
            return result['xml'],None
        else:
            if 'return_msg' in result['xml'].keys():
                return None,result['xml']['return_msg']
            elif 'retmsg' in result['xml'].keys():
                return None,result['xml']['retmsg']

    def order_refund_result(self, transaction_id='', out_trade_no='', amt = 0):
        '''
        微信退款申请
        args:
            https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_4
        '''
        headers = {'Content-Type': 'application/xml'}
        data = self.generate_refund_data(
            transaction_id=transaction_id, out_trade_no=out_trade_no, amt=amt)
        # if ' type="str"' in data:
        #     data = data.replace(' type="str"','')
        # if 'type="float"' in data:
        #     data = data.replace(' type="float"','')
        # if '<xml>b\'' in data:
        #     data = data.replace('<xml>b\'','<xml>')
        # if '</sign>\'' in data:
        #     data = data.replace('</sign>\'','</sign>')

        res = requests.post(self.REFUND_URL, data=data, headers=headers, cert=(self.WX_CERT_PATH, self.WX_KEY_PATH, self.WX_CA_PATH))
        
        if res.status_code != 200:
            return defaultdict(str),None
        try:
            result = json.loads(json.dumps(xmltodict.parse(res.content)))
            #self.logged(str(result))
            if result['xml']['return_code'] == 'SUCCESS':
                return result['xml'],None
            else:
                if 'return_msg' in result['xml'].keys():
                    return None,result['xml']['return_msg']
                elif 'retmsg' in result['xml'].keys():
                    return None,result['xml']['retmsg']
        except Exception as e:
            raise e

    def order_close_result(self,out_trade_no = ''):
        '''
        关闭订单,防止重复支付
        args:
            https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_3
        '''
        if self.DEBUG: #如果沙盒模式,不用关闭订单
            return True,None

        headers = {'Content-Type': 'application/xml'}
        params = self.default_params.copy()
        params['mch_id'] = self.mch_id
        params['nonce_str'] = self._generate_nonce_str()
        params['sign_type'] = 'MD5'

        if out_trade_no != '':
            params['out_trade_no'] = out_trade_no
        else:
            raise Exception(
                'generate_query_data need out_trade_no')

        params['sign'] = self.generate_sign(params)

        p = '<xml>%s</xml>' % dicttoxml.dicttoxml(params, root=False)

        res = requests.post(self.CLOSEORDER_URL, data=p, headers=headers)

        if res.status_code != 200:
            return defaultdict(str),None

        result = json.loads(json.dumps(xmltodict.parse(res.content)))

        if result['xml']['return_code'] == 'SUCCESS':
            return result['xml'],None
        else:
            if 'return_msg' in result['xml'].keys():
                return None,result['xml']['return_msg']
            elif 'retmsg' in result['xml'].keys():
                return None,result['xml']['retmsg']

    def verify_notify(self, **kwargs):
        u"""验证通知签名的有效性
        """
        sign = kwargs.pop('sign', '')

        if self.generate_sign(kwargs) == sign:
            return True
        else:
            return False

    def parse_notify_request(self, body):
        u"""通知请求的解析
        args:
            body: 微信异步通知的请求体
        """
        if not isinstance(body, str):
            raise Exception('body is not an xml str')

        result = json.loads(json.dumps(xmltodict.parse(body)))
        return result