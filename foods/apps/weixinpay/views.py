#encoding:utf-8
import qrcode
from django.http import HttpResponse
from django.utils.six import BytesIO
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from api.response import JsonResponse
from .pay import Wxpay
from datetime import datetime,timedelta
from django.db import transaction 

class Pay(APIView):
    '''
    调用微信的统一支付接口,获取预付信息
    '''
    def post(self,request):
        '''
        预支付
        openid : 微信授权码
        incrementId : 订单号
        notify_url : 支付后通知页面
        total_fee : 订单金额,单位为..分
        trade_type : 支付类型,JSAPI--公众号支付、NATIVE--原生扫码支付、APP--app支付
        '''
        data = request.data  
        rdata = dict()  

        if 'openid' not in data.keys() or data['openid']=='undefined' or data['openid']=='':
            return JsonResponse(code=400,desc='请先获取微信授权')
        if 'incrementId' not in data.keys() or data['incrementId']=='undefined' or data['incrementId']=='':
            return JsonResponse(code=400,desc='请确认要支付的订单号')
        if 'total_fee' not in data.keys() or data['total_fee']=='undefined' or data['total_fee']=='':
            return JsonResponse(code=400,desc='请确认订单金额')
        if 'notify_url' not in data.keys() or data['notify_url']=='undefined' or data['notify_url']=='':
            return JsonResponse(code=400,desc='请传入支付后的页面地址 例如 http://demo.ssspei.com/success.html')
        if 'trade_type' not in data.keys() or data['trade_type']=='undefined' or data['trade_type']=='':
            return JsonResponse(code=400,desc='请确认支付类型')

        wxpay = Wxpay()
        k = dict()
        k['notify_url'] = data['notify_url']
        k['body'] = 'Pay for Order %s'%data['incrementId']
        k['out_trade_no'] = data['incrementId']
        k['total_fee'] = 101 if wxpay.DEBUG else int(data['total_fee'])
        import socket
        # 获取本机计算机名称
        hostname = socket.gethostname()
        # 获取本机ip
        ip = socket.gethostbyname(hostname)
        k['spbill_create_ip'] = ip
        k['trade_type'] = data['trade_type']
        k['openid'] = data['openid']
        k['time_expire'] = (datetime.now()+timedelta(minutes=15)).strftime("%Y%m%d%H%M%S")#yyyyMMddHHmmss
        from order.models import Order
        from booking.models import BookingOrder
        try:
            order = Order.objects.get(IncrementId=k['out_trade_no'])
            if order.prepayid is not None: #如果有预付号,检测时间是否超过15分钟,如果超过则先关闭订单然后重新请求
                delta = datetime.now() - order.prepay_At
                if delta > timedelta(minutes=14):
                    cdata,error = wxpay.order_close_result(k['out_trade_no'])
                    if error is not None:
                        return JsonResponse(desc=error)
                else: #如果有预付号,位超过15分钟,返回预付号,而不请求新的
                    rdata['prepay_id'] = order.prepayid
                    if wxpay.DEBUG:
                        rdata['sandbox'] = 1
                    return JsonResponse(data=rdata)

            pdata,error = wxpay.generate_prepay_order(**k)
            if error is not None:
                return JsonResponse(desc=error)
            else:
                if 'prepay_id' in pdata.keys():                
                    order.prepayid = pdata['prepay_id']
                order.prepay_At = datetime.now()
                order.save()
                rdata = pdata
        except Order.DoesNotExist:
            order = BookingOrder.objects.get(increment_id=k['out_trade_no'])
            if order.prepayid is not None: #如果有预付号,检测时间是否超过15分钟,如果超过则先关闭订单然后重新请求
                delta = datetime.now() - order.prepay_At
                if delta > timedelta(hours=1):
                    cdata,error = wxpay.order_close_result(k['out_trade_no'])
                    if error is not None:
                        return JsonResponse(desc=error)
                else: #如果有预付号,位超过15分钟,返回预付号,而不请求新的
                    rdata['prepay_id'] = order.prepayid
                    if wxpay.DEBUG:
                        rdata['sandbox'] = 1
                        order.prepay_At = datetime.now()
                        order.paied = True
                        order.save()
                    return JsonResponse(data=rdata)

            pdata,error = wxpay.generate_prepay_order(**k)
            if error is not None:
                return JsonResponse(desc=error)
            else:
                if 'prepay_id' in pdata.keys():                
                    order.prepayid = pdata['prepay_id']
                order.prepay_At = datetime.now()
                order.save()
                rdata = pdata
        except Exception as e:
            return JsonResponse(code=400,desc=u'该订单不存在')

        if wxpay.DEBUG:
            rdata['sandbox'] = 1
        return JsonResponse(data=rdata)

class QueryWXOrder(APIView):
    '''
    查询微信订单
    '''
    @transaction.atomic()
    def post(self,request):
        '''
        查询微信订单
        openid : 微信授权码
        incrementId : 订单号
        '''
        data = request.data    

        if 'openid' not in data.keys() or data['openid']=='undefined' or data['openid']=='':
            return JsonResponse(code=400,desc='请先获取微信授权')
        if 'incrementId' not in data.keys() or data['incrementId']=='undefined' or data['incrementId']=='':
            return JsonResponse(code=400,desc='请确认要支付的订单号')

        wxpay = Wxpay()
        data,error = wxpay.order_query_result(out_trade_no=data['incrementId'])
        if error is not None:
            return JsonResponse(code=400, desc=error)
        else:
            if 'transaction_id' in data.keys():
                #引入当前项目的订单模块,完成订单支付状态的确认
                from order.models import Order
                from booking.models import BookingOrder
                from money.models import Credit
                from datetime import datetime
                try:
                    order = Order.objects.get(IncrementId=data['out_trade_no'])
                    order.Paied = True
                    order.transaction_id = data['transaction_id']
                    order.Paied_At = datetime.strptime(data['time_end'], "%Y%m%d%H%M%S")
                    order.save()
                    Credit.objects.filter(Order=order).update(is_paid=True,Closed_At=datetime.strptime(data['time_end'], "%Y%m%d%H%M%S"))
                except Order.DoesNotExist:
                    order = BookingOrder.objects.get(increment_id=data['out_trade_no'])
                    order.paied = True
                    order.transaction_id = data['transaction_id']
                    order.Paied_At = datetime.strptime(data['time_end'], "%Y%m%d%H%M%S")
                    order.save()
                except Exception as e:
                    return JsonResponse(code=400,desc=u'该订单不存在')
                #结束
            else:
                return JsonResponse(code=400,desc=data['trade_state_desc'])

            return JsonResponse(data=data)
 
class getWxPayParams(APIView):
    '''
    获取微信内H5调起支付的请求参数
    openid : 微信授权码
    prepayid : 预支付交易单
    '''
    def get(self,request):
        data = request.query_params  

        if 'openid' not in data.keys() or data.get('openid')=='undefined' or data.get('openid')=='':
            return JsonResponse(code=400,desc='请先获取微信授权')
        if 'prepayid' not in data.keys() or data.get('prepayid')=='undefined' or data.get('prepayid')=='':
            return JsonResponse(code=400,desc='该预付码已经失效,请重新提交订单,或重新支付')

        #调用微信支付
        from weixinpay.pay import Wxpay
        wxpay = Wxpay()
        params = wxpay.generate_call_jsapi_data(data.get('prepayid'))
        return JsonResponse(data=params)

class Refund(APIView):
    '''
    退款
    '''
    @transaction.atomic()
    def post(self,request):
        '''        
        openid : 微信授权码
        incrementId : 订单号
        '''
        data = request.data    

        if 'openid' not in data.keys() or data['openid']=='undefined' or data['openid']=='':
            return JsonResponse(code=400,desc='请先获取微信授权')
        if 'incrementId' not in data.keys() or data['incrementId']=='undefined' or data['incrementId']=='':
            return JsonResponse(code=400,desc='请确认要支付的订单号')

        from order.models import Order
        from booking.models import BookingOrder
        from money.models import Credit
        from datetime import datetime
        try:
            order = Order.objects.get(IncrementId=data['incrementId'])
            if order.Paied:
                wxpay = Wxpay()
                data,error = wxpay.order_refund_result(transaction_id=order.transaction_id,out_trade_no=data['incrementId'])
                if error is not None:
                    return JsonResponse(code=400, desc=error)
                             
            #确认订单取消,并删除对应的记账单
            order.Cancel_At = datetime.now()
            order.Status = 'cancel'
            order.save()
            Credit.objects.filter(Order=order).delete()
            return JsonResponse(desc=u'订单取消成功')
        except Order.DoesNotExist:
            order = BookingOrder.objects.get(increment_id=k['out_trade_no'])
            if order.Paied:
                wxpay = Wxpay()
                data,error = wxpay.order_refund_result(transaction_id=order.transaction_id,out_trade_no=data['incrementId'])
                if error is not None:
                    return JsonResponse(code=400, desc=error)
                             
            #确认订单取消,并删除对应的记账单
            order.cancel_at = datetime.now()
            order.status = 'cancel'
            order.save()
        except Exception as e:
            return JsonResponse(code=400,desc=u'该订单不存在')

            #结束
