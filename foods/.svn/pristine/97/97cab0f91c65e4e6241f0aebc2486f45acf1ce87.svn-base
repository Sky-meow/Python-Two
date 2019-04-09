#encoding:utf-8

'''
请求高德地图方法文件
'''
from urllib.parse import quote
import string
import urllib.request
import requests
import json
import foods.settings as settings

class GaoDeAPI():
    '''
    高德地图统一方法类
    '''
    def __init__(self):
        pass

    key = settings.MAP_KEY
    geofence_url = 'https://restapi.amap.com/v4/geofence/meta?key=%s'%key
    def getRequest(self,url):
        '''
        请求url返回json数组
        '''
        url = quote(url, safe=string.printable)
        temp = urllib.request.urlopen(url) 
        print(temp)
        html = temp.read()
        result = json.loads(html.decode('utf-8'),encoding='utf-8')  
        return result

    #gd_url = 'https://m.amap.com/picker/?zoom=15&center=parameter3&amp;radius=parameter4&amp;total=parameter5&amp;key=parameter6'
    def getPoint(self,address = None):
        '''
        将地址转换成坐标
        如果要批量转换,多个地址之间请用'|'隔开
        '''
        if address is None or address == '':
            return 0
        if address.find('|') > 0:
            if len(address.split('|')) > 10:
                return u'批量地址不能超过10个'
            url = 'https://restapi.amap.com/v3/geocode/geo?key=%s&address=%s&batch=true'%(self.key,address)
        else:
            url = 'https://restapi.amap.com/v3/geocode/geo?key=%s&address=%s'%(self.key,address)
        res = self.getRequest(url)
        if res['status'] == "1" and res['info'] == 'OK':
            return res['geocodes'],None  #res['geocodes'][0]['location']
        else:
            return None,res['info']

    # def checkMyPicker(self,address):
    #     '''
    #     通过客户检测指定地址附近是否有满足条件的地点(食堂)
    #     '''
    #     my_point = self.getPoint(address)

    def creategeofence(self,project = None):
        '''
        创建食堂的电子围栏
        project为想要创建围栏的项目对象或者项目id
        '''
        from store.models import store
        if type(project) == int():
            project = store.objects.select_related().get(ID=project)
        elif type(project) is store:
            pass
        else:
            return -1
        name = project.Name
        center = self.getPoint(project.Address)
        radius = int(project.Scope)*1000
        valid_time = '2054-12-31' #高德地图暂时支持2055年之前的日期
        data = {
            'name': name,
            'center': center,
            'radius': radius,
            'valid_time': valid_time,
            'repeat': 'Mon,Tues,Wed,Thur,Fri,Sat,Sun',
            'alert_condition': 'enter;leave',
            'desc': name+'配送范围'
        }
        res = requests.post(url=self.geofence_url,data=json.dumps(data))
        return json.loads(res.text,encoding='utf-8')  

    def deletegeofence(self,gid = None):
        '''
        删除电子围栏
        '''
        if gid is None:
            return -1

        res = requests.delete(url=self.geofence_url+"&gid="+gid)
        return json.loads(res.text,encoding='utf-8')  

    def getDistance(self,origins,destination,_type=0):
        '''
        获取坐标之间的距离
        默认是直线距离
        origins 起点坐标 经纬度用','分割,多个坐标用'|'分割
        destination 目的地坐标 经纬度用','分割
        type 路径计算的方式和方法 
            0：直线距离

            1：驾车导航距离（仅支持国内坐标）。

            必须指出，当为1时会考虑路况，故在不同时间请求返回结果可能不同。

            此策略和驾车路径规划接口的 strategy=4策略基本一致，策略为“ 躲避拥堵的路线，但是可能会存在绕路的情况，耗时可能较长 ”

            若需要实现高德地图客户端效果，可以考虑使用驾车路径规划接口

            2：公交规划距离（仅支持同城坐标,QPS不可超过1，否则可能导致意外）

            3：步行规划距离（仅支持5km之间的距离）
        '''
        url = 'https://restapi.amap.com/v3/distance?key=%s&origins=%s&destination=%s&type=%s'%(self.key,origins,destination,_type)
        print('***************URL**************')
        print(url)
        print('***************URL**************')
        res = self.getRequest(url)
        if res['status'] == "1" and res['info'] == 'OK':
            return res['results'],None  #res['geocodes'][0]['location']
        else:
            return None,res['info']
