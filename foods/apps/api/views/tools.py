#encoding:utf-8
import qrcode
from django.http import HttpResponse
from django.utils.six import BytesIO
from rest_framework.decorators import api_view
from api.response import JsonResponse,api_paging

'''
接口工具类
提供各种工具方法
'''
@api_view(['GET'])
def getQrcode(request,v=None):
    '''
    根据请求的值返回二维码
    '''
    img = qrcode.make(v)
 
    buf = BytesIO()
    img.save(buf)
    image_stream = buf.getvalue()

    response = HttpResponse(image_stream, content_type="image/png")
    return response

@api_view(['GET'])
def getBarcode(request,v=None):
    '''
    根据请求的值返回条码
    '''
    import barcode
    from PIL import Image
    from barcode.codex import Code39
    from barcode.writer import ImageWriter
    import io
    #EAN = barcode.get_barcode_class('ean13')
    ean = Code39(v, writer=ImageWriter(), add_checksum=False)
    fp = io.BytesIO()
    ean.write(fp)
    image_stream = fp.getvalue()
    response = HttpResponse(image_stream, content_type="image/png")
    return response
    

@api_view(['GET'])
def smsCaptcha(request,phone,key = 'bind'):
    '''
    生成短信验证码,并发送
    ---
    Parameters:
    Name: phone Description:111
    phone <b>string</b> 接收短信的手机号
    <b style="color:red">key</b>的值有: <br/>
    <b style="color:blue">bind</b> 绑定手机 <br/>
    '''
    import random, urllib.request, datetime
    from urllib.request import Request
    from urllib.parse import quote
    from django.conf import settings
    from sms.models import SmsTemplate,SmsLog
    import json
    SMSCaptcha = settings.SMSCAPTCHA
    #chars='0,1,2,3,4,5,6,7,8,9,a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z'.split(',')
    chars='0,1,2,3,4,5,6,7,8,9'.split(',')
    x = []
    for i in range(SMSCaptcha['LENGTH']):
        x.append(random.choice(chars))
    verifyCode = "".join(x)
    time = SMSCaptcha['EXPIRE']
    time = time*60
    if key is not None:
        key = "phoneVerifyCode_"+key
    else:
        key = 'phoneVerifyCode'

    #加入手机号验证,更保险
    request.session[key] = {"EXPIRE":datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "code":verifyCode,'phone':phone}
    _str = 'code:%s'%(verifyCode)
    kwarg = quote(_str,'utf-8')
    if settings.DEBUG:
        tip = u'短信发送成功,验证码是%s'%verifyCode
    else:
        templateId = SMSCaptcha['TEMPLATE']
        if key.replace('phoneVerifyCode_','') == 'bind':
            try:
                template = SmsTemplate.objects.get(key='bindphone_captch')
                templateId = template.templateId
            except:
                pass
        host = 'http://yzxtz.market.alicloudapi.com'
        path = '/yzx/notifySms'
        method = 'POST'
        #appcode = '68f3739a4e2b4794b2f9c5ba376e2294'#测试
        appcode = '87147f2c48e74c5ba6188a344a0bd1f5' #福东
        querys = 'phone=%s&templateId=%s&variable=%s'%(phone,templateId,kwarg)
        bodys = {}
        url = host + path + '?' + querys
        req = Request(url)
        req.method = method
        req.add_header('Authorization', 'APPCODE ' + appcode)
        response = urllib.request.urlopen(req)
        content = response.read()
        if (content):
            print(content)
            content = str(content,encoding='utf-8')
            content = eval(content)
            print(content)
            code = content['return_code']
            if code == '00000':
                tip = u'短信发送成功'
            elif code == '10000':
                tip = u'电话号码或者模板id为空'
            elif code =='10001':
                tip = u'手机号格式不正确'
            elif code =='10002':
                tip = u'模板不存在或模板未通过审核'
            elif code =='10003':
                tip = u'模板中包含参数,但是未传入'
            elif code == '10004':
                tip = u'模板参数中含有敏感词'
            elif code == '10005':
                tip = u'模板参数名和传入的参数名不匹配'
            elif code == '10006':
                tip = u'短信长度过长'
            elif code == '10007':
                tip = u'传入的手机号查询不到归属地'
            elif code == '10008' or code == '10009':
                tip = u'系统错误,请联系客服'
            elif code == '10010':
                tip = u'由于网络原因,重复调用了接口'
            else:
                tip = u'系统错误,请联系客服'
            tip = tip+";templateId:"+templateId
        else:
            tip = ''
    # funct = request.GET.get('callback')
    # r = '%s({"desc":"%s","code":200,"data":"%s"})'%(funct,tip,str(request.session.session_key))
    # return HttpResponse(r)
    try:
        SmsLog(key='bindphone_captch',content='短信模板:%s,发送给:%s'%(templateId,phone),reason=tip,status=code).save()
    except Exception as e:
        SmsLog(key='bindphone_captch',content=templateId,reason=e,status=code).save()
        
    if 'isIOS' in request.query_params.keys() and request.query_params.get('isIOS', False):
        data = verifyCode
    else:
        data = ''
    return JsonResponse(desc=tip,data=data)
 