#encoding:utf-8
'''
计划任务方法
'''

def checkOrderPaied():
    '''
    向微信查询订单是否已支付
    '''
    from weixinpay.pay import Wxpay
    from datetime import datetime, timedelta
    from django.db import transaction
    from django.conf import settings
    if 'booking' in settings.INSTALLED_APPS:
        from booking.models import BookingOrder
        try:
            orders = BookingOrder.objects.filter(status__in=[
                                                 'new', 'autocancel'], paied=False, booking_time__gte=datetime.now().date())
            if orders.count() > 0:
                wxpay = Wxpay()
                for order in orders:
                    with transaction.atomic():
                        data,error = wxpay.order_query_result(out_trade_no=order.increment_id)
                        if error is not None:
                            print(order.increment_id, error)
                        else:
                            if 'transaction_id' in data.keys():
                                order.paied = True
                                order.transaction_id = data['transaction_id']
                                order.Paied_At = datetime.strptime(data['time_end'], "%Y%m%d%H%M%S")
                                if order.status == 'autocancel':
                                    order.status = 'new'
                                order.save()
        except Exception as e:
            print(e)
            pass

    from order.models import Order
    try:
        orders = Order.objects.filter(Status='new',Paied=False,PayType='WeChat')
        if orders.count() > 0:
            wxpay = Wxpay()
            for order in orders:
                with transaction.atomic():
                    data,error = wxpay.order_query_result(out_trade_no=order.IncrementId)
                    if error is not None:
                        print(order.increment_id, error)
                    else:
                        if 'transaction_id' in data.keys():
                            order.Paied = True
                            order.transaction_id = data['transaction_id']
                            order.Paied_At = datetime.strptime(data['time_end'], "%Y%m%d%H%M%S")
                            order.save()
    except Exception as e:
        print(e)
        pass

def setBookingTimeOut():
    '''
    设置预订订单超时
    '''
    #from weixinpay.pay import Wxpay
    import json
    from datetime import datetime, timedelta
    from django.db import transaction
    from django.conf import settings
    if 'booking' in settings.INSTALLED_APPS:
        from booking.models import BookingOrder, ProjectsCompletion
        try:            
            store = ProjectsCompletion.objects.filter(Enable=True)
            if store.count() > 0:
                for project in store:
                    orders = BookingOrder.objects.filter(paied=True,booking_time__lte=datetime.now().date(),project = project).exclude(status__in=['cancel', 'autcancel'])         
                    if orders.count() > 0:
                        for order in orders:
                            with transaction.atomic():
                                if order.breakfast_mats is not None and order.breakfast_mats != '':
                                    breakfast_mats = json.loads(order.breakfast_mats)
                                    if breakfast_mats['status'] in ['new','confirm']:
                                        breakfast_mats['status'] = 'timeout'
                                        order.breakfast_mats = json.dumps(breakfast_mats, ensure_ascii=False)
                                
                                if order.lunch_mats is not None and order.lunch_mats != '':
                                    lunch_mats = json.loads(order.lunch_mats)
                                    if lunch_mats['status'] in ['new','confirm']:
                                        lunch_mats['status'] = 'timeout'
                                        order.lunch_mats = json.dumps(lunch_mats, ensure_ascii=False)

                                if order.dinner_mats is not None and order.dinner_mats != '':
                                    dinner_mats = json.loads(order.dinner_mats)
                                    if dinner_mats['status'] in ['new','confirm']:
                                        dinner_mats['status'] = 'timeout'
                                        order.dinner_mats = json.dumps(dinner_mats, ensure_ascii=False)
                                
                                flag = False
                                if order.breakfast_mats is not None and json.loads(order.breakfast_mats)['status'] == 'timeout':
                                    flag = True
                                else:
                                    flag = order.breakfast_mats is None
                                if order.lunch_mats is not None and json.loads(order.lunch_mats)['status'] == 'timeout':
                                    flag = True
                                else:
                                    if flag:
                                        flag = order.lunch_mats is None
                                if order.dinner_mats is not None and json.loads(order.dinner_mats)['status'] == 'timeout':
                                    flag = True
                                else:
                                    if flag:
                                        flag = order.dinner_mats is None
                                
                                if flag:
                                    order.status = 'timeout'

                                order.save()
        except Exception as e:
            print('ERROR %s' % e)
            pass

def autoCancelUnPaiedBooking():
    '''
    系统自动取消1小时未支付订单
    '''
    #from weixinpay.pay import Wxpay
    from datetime import datetime, timedelta
    from django.db import transaction
    from django.conf import settings
    if 'booking' in settings.INSTALLED_APPS:
        from booking.models import BookingOrder
        try:
            one_hour_before = (datetime.now() - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
            orders = BookingOrder.objects.filter(status='new',paied=False,created_at__lte=one_hour_before)
            if orders.count() > 0:
                count = orders.count()
                with transaction.atomic():
                    orders.update(paied=False,cancel_at=datetime.now(),status='autocancel')
                    print('***********************%s*******************' % str(datetime.now()))
                    print('CANCELED %d BOOKING ORDER SUCCESS' % count)
                    print('***********************%s*******************')
                    # for order in orders:
                    #     order.paied = False                
                    #     order.cancel_at = datetime.now()
                    #     order.status = 'autocancel'
                    #     order.save()
                    #     print('CANCEL BOOKING ORDER %s SUCCESS' % order.increment_id)
        except Exception as e:
            print('ERROR' % e)
            pass

def calcStatisticalEveryDay():
    '''
    每日计算当日完成订单的统计
    每日21点统计当天已付款的非紧急订单量
    并将结果存入统计表
    '''
    import json
    from datetime import datetime, timedelta
    from django.db import transaction
    from django.conf import settings
    if 'booking' in settings.INSTALLED_APPS:
        from booking.models import BookingOrder, ProjectsCompletion, OrderStatistical
        try:            
            store = ProjectsCompletion.objects.filter(Enable=True)
            if store.count() > 0:
                for project in store:
                    orders = BookingOrder.objects.filter(order_type=0,paied=True,booking_time=datetime.now().date(),project = project)
                    with transaction.atomic():
                        breakfast = dict()
                        lunch = dict()
                        dinner = dict()
                        for order in orders:
                            if order.breakfast_mats is not None and order.breakfast_mats != '':
                                breakfast_mats = json.loads(order.breakfast_mats)['mats']
                                for mat in breakfast_mats:
                                    p = mat['Price']
                                    if not isinstance(p, float):
                                        p = float(p)
                                    q = mat['qty']
                                    if not isinstance(q, int):
                                        q = int(q)
                                    
                                    if p not in breakfast.keys():
                                        breakfast[p] = q
                                    else:
                                        breakfast[p] += q
                            
                            if order.lunch_mats is not None and order.lunch_mats != '':
                                lunch_mats = json.loads(order.lunch_mats)['mats']
                                for mat in lunch_mats:
                                    p = mat['Price']
                                    if not isinstance(p, float):
                                        p = float(p)
                                    q = mat['qty']
                                    if not isinstance(q, int):
                                        q = int(q)
                                    
                                    if p not in lunch.keys():
                                        lunch[p] = q
                                    else:
                                        lunch[p] += q

                            if order.dinner_mats is not None and order.dinner_mats != '':
                                dinner_mats = json.loads(order.dinner_mats)['mats']
                                for mat in dinner_mats:
                                    p = mat['Price']
                                    if not isinstance(p, float):
                                        p = float(p)
                                    q = mat['qty']
                                    if not isinstance(q, int):
                                        q = int(q)
                                    
                                    if p not in dinner.keys():
                                        dinner[p] = q
                                    else:
                                        dinner[p] += q

                        blist = [OrderStatistical(project=project,date=datetime.now().date(),mealtime='breakfast',price=k,count=breakfast[k]) for k in breakfast]
                        llist = [OrderStatistical(project=project,date=datetime.now().date(),mealtime='lunch',price=k,count=lunch[k]) for k in lunch]
                        dlist = [OrderStatistical(project=project,date=datetime.now().date(),mealtime='dinner',price=k,count=dinner[k]) for k in dinner]
                         
                        if len(blist) > 0:
                            OrderStatistical.objects.bulk_create(blist)

                        if len(llist) > 0:
                            OrderStatistical.objects.bulk_create(llist)

                        if len(dlist) > 0:
                            OrderStatistical.objects.bulk_create(dlist)
                        
                        print('Statistical %s %s DATA OVER' %(str(project), datetime.now().date()))
        except Exception as e:
            print('ERROR %s' % str(e))
            pass
