import xadmin
from xadmin import views

'''
后台配置文件,仅用来做后台的配置,不写其他代码
'''

class BaseSetting(object):
    enable_themes = True #启用主题设置
    use_bootswatch = True #使用boot主题切换

class GlobalSetting(object):
    site_title = '福东饮食'   #设置头标题
    site_footer = '福东饮食'  #设置脚标题
    site_logo = '/static/images/logo.png' #设置logo路径
    menu_style = 'accordion' #可收缩列

    def get_site_menu(self):

        menu_list =  [
            {'title': '客户管理', 'menus': [
                    {'title': '客户', 'url': '/admin/customer/customer/', 'icon': None, 'perm': 'customer.view_customer', 'order': 7}, 
                    {'title': '客户签约申请记录', 'url': '/admin/customer/buesinessapply/', 'icon': None, 'perm': 'customer.view_buesinessapply', 'order': 9}
                ], 
                'first_url': '/admin/customer/customer/'
            }, 
            {'title': '收付款管理', 'menus': [
                    {'title': '记账记录', 'url': '/admin/money/credit/', 'icon': None, 'perm': 'money.view_credit', 'order': 20}, 
                    {'title': '收款记录', 'url': '/admin/money/receipt/', 'icon': None, 'perm': 'money.view_receipt', 'order': 21}
                ], 'first_url': '/admin/money/credit/'
            }, 
            {'title': '短信管理', 'menus': [
                    {'title': '短信模板', 'url': '/admin/sms/smstemplate/', 'icon': None, 'perm': 'sms.view_smstemplate', 'order': 10}, 
                    {'title': '短信日志', 'url': '/admin/sms/smslog/', 'icon': None, 'perm': 'sms.view_smslog', 'order': 11}
                ], 'first_url': '/admin/sms/smstemplate/'
            },
            {'title': '菜品管理', 'menus': [
                    #{'title': '菜品类别', 'url': '/admin/material/mattype/', 'icon': None, 'perm': 'material.view_mattype', 'order': 12}, 
                    {'title': '菜品', 'url': '/admin/material/material/', 'icon': None, 'perm': 'material.view_material', 'order': 13}, 
                    {'title': '便当', 'url': '/admin/material/bento/', 'icon': None, 'perm': 'material.view_bento', 'order': 14}
                ], 'first_url': '/admin/material/mattype/'
            }, 
            {'title': '订单管理', 'menus': [ 
                    {'title': '订单', 'url': '/admin/order/order/', 'icon': None, 'perm': 'order.view_order', 'order': 15}, 
                    {'title': '订单明细', 'url': '/admin/order/orderitems/', 'icon': None, 'perm': 'order.view_orderitems', 'order': 16}
                ], 'first_url': '/admin/order/order/'
            }, 
            {'title': '项目管理', 'menus': [
                    {'title': '项目资料', 'url': '/admin/store/store/', 'icon': None, 'perm': 'store.view_projects', 'order': 17}, 
                    {'title': '员工管理', 'url': '/admin/customer/sendingcust/', 'icon': None, 'perm': 'customer.view_sendingcust', 'order': 8}, 
                    {'title': '项目上架商品', 'url': '/admin/store/projectmats/', 'icon': 'fa fa-lock', 'perm': 'store.view_projectmats', 'order': 18},
                    {'title': '企业签约', 'url': '/admin/store/bussinessmats/', 'icon': None, 'perm': 'store.view_bussinessmats', 'order': 19},
                    {'title': '价格销量统计', 'url': '/admin/booking/orderstatistical/', 'icon': 'fa fa-bar-chart-o', 'perm': 'booking.view_orderstatistical', 'order': 20},
                    {'title': '项目每日菜谱管理', 'url': '/admin/booking/dailymenu/', 'icon': None, 'perm': 'booking.view_dailymenu', 'order': 21},
                ], 'first_url': '/admin/store/store/', 'first_icon': 'fa fa-lock'
            },
            {'title': '认证和授权', 'menus': [
                    {'title': '组', 'url': '/admin/auth/group/', 'icon': 'fa fa-group', 'perm': 'auth.view_group', 'order': 2}, 
                    {'title': '用户', 'url': '/admin/auth/user/','icon': 'fa fa-user', 'perm': 'auth.view_user', 'order': 3}, 
                    {'title': '权限', 'url': '/admin/auth/permission/', 'icon': 'fa fa-lock', 'perm': 'auth.view_permission', 'order': 4}
                ], 'first_icon': 'fa fa-group', 'first_url': '/admin/auth/group/'
            }, 
            {'title': '操作日志', 'menus': [
                    {'title': '日志记录', 'url': '/admin/xadmin/log/', 'icon': 'fa fa-cog', 'perm': 'xadmin.view_log', 'order': 6}
                ], 'first_icon': 'fa fa-cog', 'first_url': '/admin/xadmin/log/'
            }, 
            {'title': 'Reversion', 'menus': [
                    {'title': 'Revisions', 'url': '/admin/reversion/revision/', 'icon': 'fa fa-exchange', 'perm': 'reversion.view_revision', 'order': 22}
                ], 
            'first_icon':'fa fa-exchange', 'first_url': '/admin/reversion/revision/'
            }, 
        ]
        
        from django.conf import settings
        if 'booking' in settings.INSTALLED_APPS:
            booking_order = {'title': '预定订单', 'url': '/admin/booking/bookingorder/', 'icon': 'fa fa-users', 'perm': 'booking.view_bookingorder', 'order': 15}
            store = {'title': '项目资料', 'url': '/admin/booking/projectscompletion/', 'icon': None, 'perm': 'booking.view_projectscompletion', 'order': 17}

            for item in menu_list:
                if item['title'] == '订单管理':
                    item['menus'].append(booking_order)
                elif item['title'] == '项目管理':
                    for i in item['menus']:
                        if i['title'] == '项目资料':
                            i['url'] = store['url']
                            i['perm'] = store['perm']

        return menu_list

xadmin.site.register(views.CommAdminView, GlobalSetting) #注册GlobalSetting
xadmin.site.register(views.BaseAdminView, BaseSetting) #注册BaseSetting
