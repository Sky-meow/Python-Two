def smsCaptcha(session,phone,key = None):
    '''
    生成短信验证码,并发送
    '''
    import random
    import datetime
    chars='0,1,2,3,4,5,6,7,8,9,a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z'.split(',')
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

    session[key] = {"EXPIRE":datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "code":verifyCode}
    _str = 'code:%s'%(verifyCode)
    kwarg = quote(_str,'utf-8')
    if DEBUG:
        return '短信发送成功,验证码是%s'%verifyCode
    else:
        host = 'http://yzxtz.market.alicloudapi.com'
        path = '/yzx/notifySms'
        method = 'POST'
        appcode = '68f3739a4e2b4794b2f9c5ba376e2294'
        querys = 'phone=%s&templateId=%s&variable=%s'%(phone,SMSCaptcha['TEMPLATE'],kwarg)
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
                return '短信发送成功'
            elif code == '10000':
                return '电话号码或者模板id为空'
            elif code =='10001':
                return '手机号格式不正确'
            elif code =='10002':
                return '模板不存在或模板未通过审核'
            elif code =='10003':
                return '模板中包含参数,但是未传入'
            elif code == '10004':
                return '模板参数中含有敏感词'
            elif code == '10005':
                return '模板参数名和传入的参数名不匹配'
            elif code == '10006':
                return '短信长度过长'
            elif code == '10007':
                return '传入的手机号查询不到归属地'
            elif code == '10008' or code == '10009':
                return '系统错误,请联系客服'
            elif code == '10010':
                return '由于网络原因,重复调用了接口'
            else:
                return '系统错误,请联系客服'
        else:
            pass
