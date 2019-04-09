#encoding:utf-8
from django.db import transaction 
from rest_framework import serializers
from quote.models import *
from store.models import ProjectMats, ProjectMatSellOut
from store.serializers import ProjectMatsSerializers

class QuoteItemSerializers(serializers.ModelSerializer):
    '''
    购物车明细
    '''
    material = serializers.SerializerMethodField()
    def get_material(self,obj):
        '''
        获取当前购物车中的商品信息
        '''
        from datetime import datetime
        from django.db.models import Q
        from material.models import Material
        from material.serializers import MaterialSerializers
        from django.conf import settings
        project = obj.Quote.Project
        
        if 'booking' in settings.INSTALLED_APPS:
            breakfast = project.breakfast_time
            lunch = project.lunch_time
            dinner = project.dinner_time
        else:
            opentime = project.opentime.split(';')
            breakfast = opentime[0]
            lunch = opentime[1]
            dinner = opentime[2]
        now = datetime.now()
        date = now.date()
        ut = ''
        if breakfast != '':                
            starttime = date.strftime('%Y-%m-%d') +' '+breakfast.split('-')[0]
            endtime = date.strftime('%Y-%m-%d') +' '+breakfast.split('-')[1]
            if datetime.strptime(starttime,'%Y-%m-%d %H:%M') <= now and datetime.strptime(endtime,'%Y-%m-%d %H:%M') >= now:
                ut = 'breakfast'               
        if ut == '' and lunch != '':
            lendtime = date.strftime('%Y-%m-%d')+' '+lunch.split('-')[1]
            if datetime.strptime(endtime,'%Y-%m-%d %H:%M') < now and datetime.strptime(lendtime,'%Y-%m-%d %H:%M') > now:
                ut = 'lunch'    
        if ut == '' and dinner != '':
            ut = 'dinner'
        try:
            try:
                projectmats = ProjectMats.objects.select_related().filter(Q(Project=project),Q(UsedTime=ut),Q(Q(Enable_To__gte=datetime.now().strftime('%Y-%m-%d'))|Q(Enable_To__isnull=True)),Q(Enable_From__lte=datetime.now().strftime('%Y-%m-%d'))).order_by('-Enable_From','-Created_At').first()
                
                try:
                    sellout = ProjectMatSellOut.objects.select_related().get(ProjectMat=projectmats,date=datetime.now().date())
                except ProjectMatSellOut.DoesNotExist:
                    sellout = ProjectMatSellOut()
                    sellout.MatJson = ''

                matList = Material.objects.select_related().filter(project_material=projectmats).values_list('ID',flat=True)
                matList = list(matList)
            except ProjectMats.DOesNotExist:
                matList = list()
            
            data = MaterialSerializers(obj.Material).data
            if data['ID'] in matList:
                data['selling'] = 1
            else:
                data['selling'] = 0

            if str(data['ID']) in sellout.MatJson.split(','):
                data['sellout'] = 1
            else:
                data['sellout'] = 0
        except Exception as e:
            print('*******ERROR******')
            print(e)
            print('*******ERROR******')
            data = dict()

        return data

    class Meta:
        model = QuoteItem
        fields = '__all__'


class QuoteSerializers(serializers.ModelSerializer):
    '''
    商品信息
    '''
    items = serializers.SerializerMethodField()
    def get_items(self,obj):
        items = QuoteItem.objects.filter(Quote=obj).order_by('ID')
        return QuoteItemSerializers(items, many=True).data
    


    class Meta:
        model = Quote
        fields = '__all__'